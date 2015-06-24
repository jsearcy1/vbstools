import cPickle
import ROOT
from train_mlp import MLP
from random import uniform
from optparse import OptionParser
import pystyle
import pdb

def get_max(hl):
    return max([h.GetMaximum() for h in hl])*1.1

def Get_input(t):
    input_vars=[
        "Lep_pt1","Lep_eta1",
        "Lep_phi1","Lep_pt2",
        "Lep_eta2","Lep_phi2",
        "Jet_pt1","Jet_eta1",
        "Jet_phi1", "Jet_pt2",
        "Jet_eta2","Jet_phi2",
        "MEt_Et","MEt_Phi"]
    return [getattr(t,i) for i in input_vars]

if __name__=="__main__":
      parser = OptionParser()
      parser.add_option("-o", "--output", dest="out_file",
                      help="write temples to file", default="../data/ct_templates.root")
      parser.add_option("-f", dest="in_file",
                        help="inputfile file", default="../data/Output_sm.root")
      parser.add_option("-b", "--bins", dest="bins",type="int",
                      help="bins in template", default=5)
      parser.add_option( "--range", dest="range",
                      help="range of template", default="-1,1")
      parser.add_option( "--mww_cut", dest="mww_cut",
                      help="cut on mww", default="0,-1")
      parser.add_option( "--mtww_cut", dest="mtww_cut",
                      help="cut on mtww", default="0,-1")
      parser.add_option("-t", "--truth", dest="truth",type="int",
                      help="use actual cos theta instead of MLP output", default=False)
      parser.add_option("-x", "--xsec", dest="xsec",type="float",
                      help="xsec to normalize data histograms fb.", default=10)
      parser.add_option( "--MLP", dest="MLP",
                          help="pickle file with the MLP weights", default="MLPs/mlp_model.pkl")
      parser.add_option( "--var", dest="var",
                          help="pickle file with the MLP weights", default="")


      (options, args) = parser.parse_args()
      
      
      err_one=ROOT.TH1F("err1","err1",20,-2,2)
      err_two=ROOT.TH1F("err2","err2",20,-2,2)
      err_comb=ROOT.TH1F("errc","errc",20,0,2)


      err_rand_one=ROOT.TH1F("err_rand1","err_rand",20,-2,2)
      err_rand_two=ROOT.TH1F("err_rand2","err_rand",20,-2,2)
      err_rand_comb=ROOT.TH1F("err_rand_comb","err_rand_comb",20,0,2)


      out_true=ROOT.TH2F("true","true",20,-1,1,20,-1,1)      
      out_pred=ROOT.TH2F("pred","pred",20,-1,1,20,-1,1)
      
      
      classifier=cPickle.load(open(options.MLP,"rb"))
      rf=ROOT.TFile(options.in_file)
      n_bins=options.bins

      t=rf.Get("Test")
      x=classifier.input_v
      
      n_evt=t.GetEntries()/100.

      if n_evt > t.GetEntries()/2:
          n_evt = t.GetEntries()/2.


      for evt in xrange(n_evt*2):#*2 is for even/odd removal
          
          if evt %2 !=0: continue #even events for analysis
          t.GetEntry(evt)
          ct1,ct2=classifier.output.eval({x:[Get_input(t)]})[0]
          out_true.Fill(t.ct1,t.ct2)
          out_pred.Fill(ct1,ct2)
          
          if (t.ct1-ct1)**2+(t.ct2-ct2)**2 < (t.ct1-ct2)**2+(t.ct2-ct1)**2:
              
              err_comb.Fill( ((t.ct1-ct1)**2+(t.ct2-ct2)**2 )**.5)
              err_one.Fill( t.ct1-ct1 )
              err_two.Fill(  t.ct2-ct2 )
          else:
              err_comb.Fill( ((t.ct1-ct2)**2+(t.ct2-ct1)**2 )**.5)
              err_one.Fill( t.ct1-ct2 )
              err_two.Fill(  t.ct2-ct1 )

          rct1=uniform(-1,1)
          rct2=uniform(-1,1)
          if (t.ct1-rct1)**2+(t.ct2-rct2)**2 < (t.ct1-rct2)**2+(t.ct2-rct1)**2:              
              err_rand_comb.Fill( ((t.ct1-rct1)**2+(t.ct2-rct2)**2 )**.5)
              err_rand_one.Fill( t.ct1-rct1 )
              err_rand_two.Fill(  t.ct2-rct2 )
          else:
              err_rand_comb.Fill( ((t.ct1-rct2)**2+(t.ct2-rct1)**2 )**.5)
              err_rand_one.Fill( t.ct1-rct2 )
              err_rand_two.Fill(  t.ct2-rct1 )



ROOT.TCanvas()
x=out_pred.ProjectionX()
x2=out_true.ProjectionX()
maxi=max([x.GetMaximum(),x2.GetMaximum()])*1.1

c1=ROOT.TCanvas()
l1=ROOT.TLegend(0.2,0.7,0.4,0.8)
l1.SetFillColor(ROOT.kWhite)
l1.SetLineColor(ROOT.kWhite)
l1.AddEntry(x,"NN Prediction")
l1.AddEntry(x2,"Truth")
x.SetLineColor(ROOT.kGreen)
x2.SetLineColor(ROOT.kBlack)
x2.SetXTitle("cos(#theta^{*})")
x2.SetYTitle("A.U.")
x2.SetMinimum(0)
x2.SetMaximum(maxi)
x2.SetMaximum(get_max([x,x2]))
x2.Draw()
x.Draw("same")
l1.Draw()
c1.SaveAs("plots/OneD_cts_compare.root")


c2=ROOT.TCanvas()

l2=ROOT.TLegend(0.6,0.6,0.8,0.8)
l2.SetFillColor(ROOT.kWhite)
l2.SetLineColor(ROOT.kWhite)
l2.AddEntry(err_comb,"NN Prediction")
l2.AddEntry(err_rand_comb,"Random Guess")

err_rand_comb.SetYTitle("A.U.")
err_rand_comb.SetXTitle("#sqrt{((cos#theta*_{NN,1}-cos#theta*_{True,1})^{2}+(cos#theta*_{NN,2}-cos#theta*_{True,2})^{2})}")
err_rand_comb.SetLineColor(ROOT.kRed)
err_rand_comb.SetMaximum(get_max([err_rand_comb,err_comb]))
err_rand_comb.Draw()

err_comb.Draw("same")
l2.Draw()
c2.SaveAs("plots/OneD_cts_err.root")


c3=ROOT.TCanvas()
err_one.SetXTitle("cos#theta*_{NN} - cos#theta*_{True}")
err_one.SetYTitle("A.U.")
err_rand_one.SetLineColor(ROOT.kRed)
err_one.SetMaximum(get_max([err_one,err_rand_one]))
err_one.Draw()
err_rand_one.Draw("same")


l3=ROOT.TLegend(0.6,0.6,0.8,0.8)
l3.SetFillColor(ROOT.kWhite)
l3.SetLineColor(ROOT.kWhite)
l3.AddEntry(err_one,"NN Prediction")
l3.AddEntry(err_rand_one,"Random Guess")
l3.Draw()
c3.SaveAs("plots/cts_dist.root")

pdb.set_trace()
c1.SaveAs("plots/OneD_cts_compare.pdf")
c2.SaveAs("plots/OneD_cts_compare.pdf")
c3.SaveAs("plots/cts_dist.pdf")
