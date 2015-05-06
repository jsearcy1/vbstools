import ROOT
from array import array
import sys
from pol_tools import *
import pdb

"""Usage: python fit.py in_file.root out_file.root
This fits cos theta distributions to analitcaly functions and plots the fraction"""

if __name__=="__main__":

    
      start=0
      end=3000
      bins=30

      m=ROOT.TH1F("M","M",50,78,82)
      cost=ROOT.TH1F("cts","cts",20,-0.8,1)
      n_x=20
      n_y=20
      ## Book histograms
      cost2D=ROOT.TH2F("cts2","cts2",n_x,-.8,1,bins,start,end)
      Mjj1=ROOT.TH1F("fr","fr",bins,start,end)
      Mjj2=ROOT.TH1F("fl","fl",bins,start,end)
      Mjj3=ROOT.TH1F("fo","fo",bins,start,end)
      tHist=ROOT.TH1F("MWjj","MWjj",1000,0,1000)

      H_frac_func=ROOT.TF1("hff","[0]*3/8*((1+x^2)+1/2*[1]*(1-3*x^2)+[2]*x )",-1,1)
      H_frac_func2=ROOT.TF2("hff2","[0]*9/64*((1+x^2)+1/2*[1]*(1-3*x^2)+[2]*x )*((1+y^2)+1/2*[3]*(1-3*y^2)+[4]*y ) ",-2,2)

      fit_func=ROOT.TF1("cts","(3/8*(1-x)^2*[0] +3/8*(1+x)^2*[1]+3/4*(1-x^2)*[2])",-.8,1)
      fit_func2=ROOT.TF2("cts2","[0]*(3/8*(1-x)^2*[1] +3/8*(1+x)^2*[2]+3/4*(1-x^2)*[3])*(3/8*(1-y)^2*[4] +3/8*(1+y)^2*[5]+3/4*(1-y^2)*[6])",-2,2)

      ## Analytic fitting functions

      fl=ROOT.TF1("fl","[0]*(3/8*(1-x)^2*[1])",-1,1)
      fr=ROOT.TF1("fr","[0]*(3/8*(1+x)^2*[1])",-1,1)
      f0=ROOT.TF1("f0","[0]*(3/4*(1-x^2)*[1])",-1,1)


      rf_infile=sys.argv[1]
      rf_in=ROOT.TFile(rf_infile)
      tree=rf_in.Get("Test")

      fit_func.SetParameter(0,cost.Integral())


      fit_func.SetParameter(0,.33)
      fit_func.SetParameter(1,.33)
      fit_func.SetParameter(2,.33)

      fit_func.SetParLimits(0,0,1)
      fit_func.SetParLimits(1,0,1)
      fit_func.SetParLimits(2,0,1)

      fit_func2.SetParameter(0,cost.Integral())
      fit_func2.SetParameter(1,.33)
      fit_func2.SetParameter(2,.33)
      fit_func2.SetParameter(3,.33)
      fit_func2.SetParameter(4,.33)
      fit_func2.SetParameter(5,.33)
      fit_func2.SetParameter(6,.33)


      #tree.SetBranchStatus("*",0)
      #tree.SetBranchStatus("ct*",1)

      for evt in range(tree.GetEntries()):
          tree.GetEntry(evt)
      #    cost2D.Fill(tree.ct1,tree.ct2)
          jet1=ROOT.TLorentzVector()
          jet2=ROOT.TLorentzVector()

          l1=ROOT.TLorentzVector()
          l2=ROOT.TLorentzVector()

          n1=ROOT.TLorentzVector()
          n2=ROOT.TLorentzVector()


          l1.SetPtEtaPhiM(tree.Lep_pt1,tree.Lep_eta1,tree.Lep_phi1,0)
          l2.SetPtEtaPhiM(tree.Lep_pt2,tree.Lep_eta2,tree.Lep_phi2,0)

          jet1.SetPtEtaPhiM(tree.Jet_pt1,tree.Jet_eta1,tree.Jet_phi1,0)
          jet2.SetPtEtaPhiM(tree.Jet_pt2,tree.Jet_eta2,tree.Jet_phi2,0)

          n1.SetPtEtaPhiM(tree.Nu_pt1,tree.Nu_eta1,tree.Nu_phi1,0)
          n2.SetPtEtaPhiM(tree.Nu_pt2,tree.Nu_eta2,tree.Nu_phi2,0)
          pt1=(l1+n1).Pt()
          pt2=(l2+n2).Pt()
          mjj=(jet1+jet2).M()
          tHist.Fill(pt1)
          tHist.Fill(pt2)
          if mjj < 150:        
      #    tHist.Fill((jet1+jet2+l1+n1).M())
        #  tHist.Fill((jet1+jet2+l2+n2).M())
           continue
          R=tree.Lep_pt1/tree.Jet_pt1*tree.Lep_pt2/tree.Jet_pt2

      #    cost2D.Fill(tree.ct1,R)
      #    cost2D.Fill(tree.ct2,R)

          cost2D.Fill(tree.ct1,tree.Mww)
          cost2D.Fill(tree.ct2,tree.Mww)
      #    cost2D.Fill(tree.ct1,pt1)
      #    cost2D.Fill(tree.ct2,pt2)

      #    cost2D.Fill(tree.ct1,mjj)
      #    cost2D.Fill(tree.ct2,mjj)

      #    pdb.set_trace()
      cost2D.Fit("hff2")
      cost2D.Draw("colz")
      h_helper=[]
      c1=ROOT.TCanvas()
      start=False
      for i in range(bins+1):
          x=cost2D.ProjectionX("b_"+str(i),i,i);
          x.Sumw2()
          if x.Integral(0,1000)==0:continue
          x.Scale(1/x.Integral(0,1000))
          x.Fit("cts");
          x.Draw();
          h_helper.append(x)

          fl=ROOT.TF1("fl","(3/8*(1-x)^2*[0])",-1,1)
          fr=ROOT.TF1("fr","(3/8*(1+x)^2*[0])",-1,1)
          f0=ROOT.TF1("f0","(3/4*(1-x^2)*[0])",-1,1)
          fl.SetParameter(0,fit_func.GetParameter(0))
          fr.SetParameter(0,fit_func.GetParameter(1))
          f0.SetParameter(0,fit_func.GetParameter(2))
          fl.Draw("same")
          fr.Draw("same")
          f0.Draw("same")
          fac=1./x.GetXaxis().GetBinWidth(4)

          Mjj3.SetBinContent(i,fit_func.GetParameter(2)*fac)
          Mjj3.SetBinError(i,fit_func.GetParError(2)*fac)

          Mjj1.SetBinContent(i,fit_func.GetParameter(0)*fac)
          Mjj1.SetBinError(i,fit_func.GetParError(0)*fac)

          Mjj2.SetBinContent(i,fit_func.GetParameter(1)*fac)
          Mjj2.SetBinError(i,fit_func.GetParError(1)*fac)

          Mjj3.SetMarkerColor(ROOT.kRed)
          Mjj3.SetLineColor(ROOT.kRed)


          if start:
              x.Draw()
              start=False
          x.Draw("same")

      c2=ROOT.TCanvas()
      Mjj1.Draw()
      Mjj2.Draw("same")
      Mjj3.Draw("same")

      rf_out=ROOT.TFile(sys.argv[2],"Recreate")
      rf_out.cd()
      Mjj1.Write()
      Mjj2.Write()
      Mjj3.Write()
      cost2D.Write()
