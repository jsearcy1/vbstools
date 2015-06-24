import cPickle
import ROOT
from train_mlp import *
import random
from optparse import OptionParser

def LepPtRatio(t):
    if t.Lep_pt1>t.Lep_pt2:
        return t.Lep_pt2/t.Lep_pt1
    return t.Lep_pt1/t.Lep_pt2
def PolRatio(t):
    return (t.Lep_pt1*t.Lep_pt2)/(t.Jet_pt1*t.Jet_pt2)

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

global rf_ff,h_fl,h_fr,h_fo
rf_ff=ROOT.TFile("../fitted_factions.root")
h_fl=rf_ff.Get("fr")#I need to fix this these hists are switched in root file
h_fr=rf_ff.Get("fl")
h_fo=rf_ff.Get("fo")

def recal_w(t):
    charge=t.Lep_charge1 #1 and 2 are equal for ssWW

    bin=h_fl.FindBin(t.Mww)
    if bin >= h_fl.GetNbinsX():
        bin=h_fl.GetNbinsX()
    

    ct1=t.ct1
    ct2=t.ct2

    fr=h_fr.GetBinContent(bin)
    fl=h_fl.GetBinContent(bin)
    f0=h_fo.GetBinContent(bin)

#    fr=0.4245
#    fl=0.3237
#    f0=0.2518

#    fl=0.36135634238668457
#    fr=0.34566328824714387
#    fo=0.2925406254842256


    norm= (  ( fl*(3./8.*(1-ct1*charge)**2) +fr*(3./8.*(1+ct1*charge)**2)+f0*(3./4.*(1-ct1**2))  )
             * (  fl*(3./8.*(1-ct2)**2) +fr*(3./8.*(1+ct2)**2)+ f0*(3./4.*(1-ct2**2))  ) )
    if norm==0: 
#        print "normalization is 0 this should never happen, dumping to debug shell"
        t.OOw=1
        t.LLw=1
        t.RRw=1
        t.LRw=1
        t.OLw=1
        t.ORw=1       
        return
#        pdb.set_trace() 
    t.OOw=((3./4.*(1-ct1**2)*f0)*(3./4.*(1-ct2**2)*f0 ))/norm
    t.LLw=((3./8.*(1-ct1*charge)**2*fl)*(3./8.*(1-ct2)**2*fl))/norm
    t.RRw=((3./8.*(1+ct1*charge)**2)*fr*(3./8.*(1+ct2)**2*fr))/norm
    t.LRw=(((3./8.*(1-ct1*charge)**2*fl+3./8.*(1+ct1*charge)**2*fr) * (3./8.*(1-ct2)**2*fl +3./8.*(1+ct2)**2*fr))/norm-t.LLw-t.RRw)
   
    t.OLw=((3./8.*(1-ct1*charge)**2*fl)*(3./4.*(1-ct2**2)*f0)+(3./4.*(1-ct1**2)*f0)*(3./8.*(1-ct2)**2*fl))/norm
    t.ORw=((3./8.*(1+ct1*charge)**2*fr)*(3./4.*(1-ct2**2)*f0)+(3./4.*(1-ct1**2)*f0)*(3./8.*(1+ct2)**2*fr))/norm
    #t.TTw=(3./8.*(1-ct1*charge)**2*fl+3./8.*(1+ct1*charge)**2*fr)*(3./8.*(1-ct2)**2*fl +3./8.*(1+ct2)**2*fr)/norm
    #t.TOw=(3./8.*(1-ct1*charge)**2*fl+3./8.*(1+ct1*charge)**2*fr)*(3./4.*(1-ct2**2)*f0)+(3./8.*(1-ct2)**2*fl +3./8.*(1+ct2)**2*fr)*(3./4.*(1-ct1**2)*f0)/norm
    
#    if t.OOw+t.LLw+t.RRw+t.LRw+t.OLw+t.ORw != 1: 
#        print  t.OOw+t.LLw+t.RRw+t.LRw+t.OLw+t.ORw 
#        pdb.set_trace()

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
                      help="xsec to normalize data histograms fb.", default=8.4)
      parser.add_option( "--MLP", dest="MLP",
                          help="pickle file with the MLP weights", default="MLPs/mlp_model.pkl")
      parser.add_option( "--var", dest="var",
                          help="pickle file with the MLP weights", default="")
      parser.add_option( "--cuts", dest="cuts",type="int",
                         help="use atlas cuts", default=0)


      (options, args) = parser.parse_args()
      
      
      
      classifier=cPickle.load(open(options.MLP,"rb"))
      rf=ROOT.TFile(options.in_file)
      n_bins=options.bins

      t=rf.Get("Test")
      x=classifier.input_v
      weights=["OOw","LRw","RRw","LLw","OLw","ORw"]
      hists=[]
      h_start,h_stop=[float(i) for i in options.range.split(",")]

      for weight in weights:
          if options.var=="": # 2D ct1 histograms
              exec "h_"+weight.strip("w")+"=ROOT.TH2F('"+weight+"','"+weight+"',n_bins,h_start,h_stop,n_bins,h_start,h_stop)"
          else: ## assume genearic vars are 1d
              exec "h_"+weight.strip("w")+"=ROOT.TH1F('"+weight+"','"+weight+"',n_bins,h_start,h_stop)"
          exec "hists.append(h_"+weight.strip("w")+")"
  

      ## For one D f
      h_L=ROOT.TH1F("L","L",n_bins,h_start,h_stop)   
      h_R=ROOT.TH1F("R","R",n_bins,h_start,h_stop)   
      h_O=ROOT.TH1F("O","O",n_bins,h_start,h_stop)   
      h_norm1d=ROOT.TH1F("nor","nor",n_bins,h_start,h_stop)   
      h_ctsb=ROOT.TH1F("cts_b","cts_b",n_bins,-1,1)   
      h_ctsa=ROOT.TH1F("cts_a","cts_a",n_bins,-1,1)   
      
      if options.var!="":
          norm=ROOT.TH1F("norm","norm",n_bins,h_start,h_stop)
      else:
          norm=ROOT.TH2F("norm","norm",n_bins,h_start,h_stop,n_bins,h_start,h_stop)
          
      diff=ROOT.TH1F("diff","diff",50,0,2)
      diffr=ROOT.TH1F("diffr","diffr",50,0,2)
      #t.GetEntries()
      j1=ROOT.TLorentzVector()
      j2=ROOT.TLorentzVector()
      l1=ROOT.TLorentzVector()
      l2=ROOT.TLorentzVector()
      met=ROOT.TLorentzVector()
      
      mt_low,mt_high=[float(i) for i in options.mtww_cut.split(",")]
      if mt_high==-1:
          mt_high=1000000000000000000
      mww_low,mww_high=[float(i) for i in options.mww_cut.split(",")]
      if mt_high==-1:
          mt_high=1000000000000000000
      if mww_high==-1:
          mww_high=1000000000000000000

      tmp=ROOT.TH1F("m","m",300,0,3000)
      
      n_evt=t.GetEntries()


#      n_evt=100000
      if n_evt > t.GetEntries()/2:
          n_evt = t.GetEntries()/2.
      xsec_w=options.xsec/n_evt #these shouldn't be weighted

      if options.var!="":
          exec "template_func=" + options.var
      else:
          template_func=None

      for evt in xrange(n_evt*2):#*2 is for even/odd removal
          
          if evt %2 !=0: continue #even events for analysis
          ###Clip trick events for a test
          ###
          t.GetEntry(evt)
          recal_w(t)
#          if t.ct1<-0.8 or t.ct2 < -0.8:continue
          h_ctsb.Fill(t.ct1)
          h_ctsb.Fill(t.ct2)
          if mww_low > t.Mww:continue
          if mww_high < t.Mww:continue
          if 0 in [t.Jet_pt1,t.Jet_eta1,t.Jet_phi1,
                   t.Jet_pt2,t.Jet_eta2,t.Jet_phi2,
                   t.Lep_pt1,t.Lep_eta1,t.Lep_phi1,
                   t.Lep_pt1,t.Lep_eta1,t.Lep_phi1]:continue #event lost to delphes reco

#          Pt Cuts
          j1.SetPtEtaPhiM(t.Jet_pt1,t.Jet_eta1,t.Jet_phi1,0.)
          j2.SetPtEtaPhiM(t.Jet_pt2,t.Jet_eta2,t.Jet_phi2,0.)
          l1.SetPtEtaPhiM(t.Lep_pt1,t.Lep_eta1,t.Lep_phi1,0.)
          l2.SetPtEtaPhiM(t.Lep_pt2,t.Lep_eta2,t.Lep_phi2,0.)

          if options.cuts==1 or options.cuts==7:
              if t.Jet_pt1 < 30: continue
              if t.Jet_pt2 < 30: continue

              if t.Lep_pt1 < 25: continue
              if t.Lep_pt2 < 25: continue
              if t.MEt_Et < 40: continue
              if (j1+j1).M() > 500: continue
              if abs(j1.Rapidity()-j2.Rapidity()) < 2.4:continue
          if options.cuts ==7:#tight Jet cuts
              if t.Jet_pt1 < 60: continue
              if t.Jet_pt2 < 60: continue


          if options.cuts==2: # no MET
              if t.Jet_pt1 < 30: continue
              if t.Jet_pt2 < 30: continue
              if t.Lep_pt1 < 25: continue
              if t.Lep_pt2 < 25: continue
              if (j1+j1).M() > 500: continue
              if abs(j1.Rapidity()-j2.Rapidity()) < 2.4:continue

          if options.cuts==3: # no rapididty
              if t.Jet_pt1 < 30: continue
              if t.Jet_pt2 < 30: continue
              if t.Lep_pt1 < 25: continue
              if t.Lep_pt2 < 25: continue
              if (j1+j1).M() > 500: continue

          if options.cuts==4: # no Mjj
              if t.Jet_pt1 < 30: continue
              if t.Jet_pt2 < 30: continue
              if t.Lep_pt1 < 25: continue
              if t.Lep_pt2 < 25: continue

          if options.cuts==5: # low pt
              if t.Jet_pt1 < 20: continue
              if t.Jet_pt2 < 20: continue
              if t.Lep_pt1 < 20: continue
              if t.Lep_pt2 < 20: continue

          if options.cuts==6: # lower pt
              if t.Jet_pt1 < 20: continue
              if t.Jet_pt2 < 20: continue
              if t.Lep_pt1 < 10: continue
              if t.Lep_pt2 < 10: continue



          


          met.SetPtEtaPhiM(t.MEt_Et,0.,t.MEt_Phi,0)
          mass=(l1+l2+met)
          tmp.Fill(mass.M())
          
          if mt_low > mass.M():continue
          if mt_high < mass.M():continue



          h_ctsa.Fill(t.ct1)
          h_ctsa.Fill(t.ct2)

          if template_func!=None: ### if you want to put in a generic function
              var=template_func(t)
          elif options.truth:      #This is a closure test type of thing
                  ct1=t.ct1
                  ct2=t.ct2
          else:
              ct1,ct2=classifier.output.eval({x:[Get_input(t)]})[0]
          if template_func:              
              norm.Fill(var,xsec_w) 
              for weight,hist in zip(weights,hists):
                  hist.Fill(var,getattr(t,weight)*xsec_w)
              h_norm1d.Fill(var,xsec_w)
              h_L.Fill(var,(t.LLw+t.OLw/2.+t.LRw/2.)*xsec_w)   
              h_R.Fill(var,(t.RRw+t.ORw/2.+t.LRw/2.)*xsec_w)   
              h_O.Fill(var,(t.OOw+t.OLw/2.+t.ORw/2.)*xsec_w)   


          else:
              for weight,hist in zip(weights,hists):
                  hist.Fill(ct1,ct2,getattr(t,weight)*xsec_w)
              norm.Fill(ct1,ct2,xsec_w) 
              h_norm1d.Fill(ct1,xsec_w)
              h_norm1d.Fill(ct2,xsec_w)
              h_L.Fill(ct1,(t.LLw+t.OLw/2.+t.LRw/2.)*xsec_w)   
              h_L.Fill(ct2,(t.LLw+t.OLw/2.+t.LRw/2.)*xsec_w)   
              h_R.Fill(ct1,(t.RRw+t.ORw/2.+t.LRw/2.)*xsec_w)   
              h_R.Fill(ct2,(t.RRw+t.ORw/2.+t.LRw/2.)*xsec_w)   
              h_O.Fill(ct1,(t.OOw+t.OLw/2.+t.ORw/2.)*xsec_w)   
              h_O.Fill(ct2,(t.OOw+t.OLw/2.+t.ORw/2.)*xsec_w)                 
      #    diff.Fill(((ct1-t.ct1)**2+(ct2-t.ct2)**2)**.5)
      #    diffr.Fill(((ct1-random.uniform(h_start,h_stop))**2+(ct2-random.uniform(h_start,h_stop))**2)**.5)


      #htt.DrawNormalized()
      #hoo.DrawNormalized"same")
      out_rf=ROOT.TFile(options.out_file,"Recreate")
      out_rf.cd()
      h_L.Write()
      h_R.Write()
      h_O.Write()
      norm.Write()
      h_ctsa.Write()
      h_ctsb.Write()
      h_norm1d.Write()
      for h in hists:
          h.Write()


