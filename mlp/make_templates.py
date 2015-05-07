import cPickle
import ROOT
from train_mlp import *
import random

classifier=cPickle.load(open("MLPs/mlp_model.pkl","rb"))
rf=ROOT.TFile("../data/Output_sm.root")

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
n_bins=20

t=rf.Get("Test")
x=classifier.input_v
weights=["OOw","LRw","RRw","LLw","OLw","ORw"]
hists=[]
for weight in weights:
    exec "h_"+weight.strip("w")+"=ROOT.TH2F('"+weight+"','"+weight+"',n_bins,-1,1,n_bins,-1,1)"
    exec "hists.append(h_"+weight.strip("w")+")"

#htt=ROOT.TH2F("TT","TT",n_bins,-1,1,n_bins,-1,1)
#hot=ROOT.TH2F("OT","OT",n_bins,-1,1,n_bins,-1,1)

## For one D f
h_L=ROOT.TH1F("L","L",n_bins*2,-1.0,1.0)   
h_R=ROOT.TH1F("R","R",n_bins*2,-1.0,1.0)   
h_O=ROOT.TH1F("O","O",n_bins*2,-1.0,1.0)   
h_norm1d=ROOT.TH1F("nor","nor",n_bins*2,-1,1)   

#httr=ROOT.TH1F("TTr","TTr",50,0,1)
#hoor=ROOT.TH1F("OOr","OOr",50,0,1)
norm=ROOT.TH2F("norm","norm",n_bins,-1,1,n_bins,-1,1)


diff=ROOT.TH1F("diff","diff",50,0,2)
diffr=ROOT.TH1F("diffr","diffr",50,0,2)
#t.GetEntries()
j1=ROOT.TLorentzVector()
j2=ROOT.TLorentzVector()



for evt in xrange(40000):
    t.GetEntry(evt)
    j1.SetPtEtaPhiM(t.Jet_pt1,t.Jet_eta1,t.Jet_phi1,0.)
    j2.SetPtEtaPhiM(t.Jet_pt2,t.Jet_eta2,t.Jet_phi2,0.)
    if (j1+j1).M() > 500: continue

    ct1,ct2=classifier.output.eval({x:[Get_input(t)]})[0]
#This is a closure test type of thing
#    ct1=t.ct1
#    ct2=t.ct2
    for weight,hist in zip(weights,hists):
        hist.Fill(ct1,ct2,getattr(t,weight))

#    hoo.Fill(ct1,ct2,t.OOw)
#    htt.Fill(ct1,ct2,t.TTw)
#    hoor.Fill((ct1**2+ct2**2)**.5,t.OOw)
#    httr.Fill((ct1**2+ct2**2)**.5,t.TTw)
#    if random.random() >.975: 
    norm.Fill(ct1,ct2) #sum fewer number of events
    h_norm1d.Fill(ct1)
    h_norm1d.Fill(ct2)
    h_L.Fill(ct1,t.LLw)   
    h_L.Fill(ct2,t.LLw)   

    h_R.Fill(ct1,t.RRw)   
    h_R.Fill(ct2,t.RRw)   

    h_O.Fill(ct1,t.OOw)   
    h_O.Fill(ct2,t.OOw)   


#    diff.Fill(((ct1-t.ct1)**2+(ct2-t.ct2)**2)**.5)
#    diffr.Fill(((ct1-random.uniform(-1,1))**2+(ct2-random.uniform(-1,1))**2)**.5)


#htt.DrawNormalized()
#hoo.DrawNormalized"same")
out_rf=ROOT.TFile("ct_templates.root","Recreate")
out_rf.cd()
h_L.Write()
h_R.Write()
h_O.Write()
norm.Write()
h_norm1d.Write()
for h in hists:
    h.Write()


