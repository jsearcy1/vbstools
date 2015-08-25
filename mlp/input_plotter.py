import cPickle
import ROOT
import random
from optparse import OptionParser
import sys
import numpy as np

if sys.argv[1] == "-i":
    filename = sys.argv[2]
    decay_filename = sys.argv[3]
else:
    filename = sys.argv[1]
    decay_filename = sys.argv[2]

rf=ROOT.TFile(filename)
rf_decay = ROOT.TFile(decay_filename)

t=rf.Get("Test")
t_decay = rf_decay.Get("Test")

n_evt=t.GetEntries()
n_evt_decay=t_decay.GetEntries()

hist_pt1 = ROOT.TH1F("ha","pt1",100,0,1000)
hist_eta1 = ROOT.TH1F("hm","eta1",100,-10,10)
hist_phi1 = ROOT.TH1F("huh","phi1",100,-10,10)
hist_pt2 = ROOT.TH1F("ho","pt2",100,0,1000)
hist_eta2 = ROOT.TH1F("hu","eta2",100,-10,10)
hist_phi2 = ROOT.TH1F("he","phi2",100,-10,10)
hist_jetpt1 = ROOT.TH1F("hy","jetpt1",100,0,1000)
hist_jeteta1 = ROOT.TH1F("hh","jeteta1",100,-10,10)
hist_jetphi1 = ROOT.TH1F("hum","jetphi1",100,-10,10)
hist_jetpt2 = ROOT.TH1F("hurr","jetpt2",100,0,1000)
hist_jeteta2 = ROOT.TH1F("hey","jeteta2",100,-10,10)
hist_jetphi2 = ROOT.TH1F("him","jetphi2",100,-10,10)
hist_met = ROOT.TH1F("hi","met",100,0,1000)
hist_mphi = ROOT.TH1F("hee","mphi",100,-10,10)

dhist_pt1 = ROOT.TH1F("things","pt1",100,0,1000)
dhist_eta1 = ROOT.TH1F("have","eta1",100,-10,10)
dhist_phi1 = ROOT.TH1F("changed","phi1",100,-10,10)
dhist_pt2 = ROOT.TH1F("for","pt2",100,0,1000)
dhist_eta2 = ROOT.TH1F("me","eta2",100,-10,10)
dhist_phi2 = ROOT.TH1F("and","phi2",100,-10,10)
dhist_jetpt1 = ROOT.TH1F("that's","jetpt1",100,0,1000)
dhist_jeteta1 = ROOT.TH1F("okay","jeteta1",100,-10,10)
dhist_jetphi1 = ROOT.TH1F("I","jetphi1",100,-10,10)
dhist_jetpt2 = ROOT.TH1F("feel","jetpt2",100,0,1000)
dhist_jeteta2 = ROOT.TH1F("the","jeteta2",100,-10,10)
dhist_jetphi2 = ROOT.TH1F("same","jetphi2",100,-10,10)
dhist_met = ROOT.TH1F("I'm on my way","met",100,0,1000)
dhist_mphi = ROOT.TH1F("and I say","mphi",100,-10,10)

reg_weight = 8.4/n_evt
D_weight = 11.64/n_evt_decay

for evt in xrange(n_evt):
    t.GetEntry(evt)
    if t.Lep_pt1 == 0 or t.Lep_pt2 == 0 or t.Jet_pt1 == 0 or t.Jet_pt2 == 0 or t.Lep_pt1 < 10 or t.Lep_pt2 < 10 or t.Lep_eta1 > 2.5 or t.Lep_eta1 < -2.5 or t.Lep_eta2 > 2.5 or t.Lep_eta2 < -2.5: continue
    hist_pt1.Fill(t.Lep_pt1,reg_weight)
    hist_eta1.Fill(t.Lep_eta1,reg_weight)
    hist_phi1.Fill(t.Lep_phi1,reg_weight)
    hist_pt2.Fill(t.Lep_pt2,reg_weight)
    hist_eta2.Fill(t.Lep_eta2,reg_weight)
    hist_phi2.Fill(t.Lep_phi2,reg_weight)
    hist_jetpt1.Fill(t.Jet_pt1,reg_weight)
    hist_jeteta1.Fill(t.Jet_eta1,reg_weight)
    hist_jetphi1.Fill(t.Jet_phi1,reg_weight)
    hist_jetpt2.Fill(t.Jet_pt2,reg_weight)
    hist_jeteta2.Fill(t.Jet_eta2,reg_weight)
    hist_jetphi2.Fill(t.Jet_phi2,reg_weight)
    hist_met.Fill(t.MEt_Et,reg_weight)
    hist_mphi.Fill(t.MEt_Phi,reg_weight)

for evt in xrange(n_evt_decay):
    t_decay.GetEntry(evt)
    if t_decay.Lep_pt1 == 0 or t_decay.Lep_pt2 == 0 or t_decay.Jet_pt1 == 0 or t_decay.Jet_pt2 == 0 or t_decay.Lep_pt1 < 10 or t_decay.Lep_pt2 < 10 or t_decay.Lep_eta1 > 2.5 or t_decay.Lep_eta1 < -2.5 or t_decay.Lep_eta2 > 2.5 or t_decay.Lep_eta2 < -2.5: continue
    dhist_pt1.Fill(t_decay.Lep_pt1,D_weight)
    dhist_eta1.Fill(t_decay.Lep_eta1,D_weight)
    dhist_phi1.Fill(t_decay.Lep_phi1,D_weight)
    dhist_pt2.Fill(t_decay.Lep_pt2,D_weight)
    dhist_eta2.Fill(t_decay.Lep_eta2,D_weight)
    dhist_phi2.Fill(t_decay.Lep_phi2,D_weight)
    dhist_jetpt1.Fill(t_decay.Jet_pt1,D_weight)
    dhist_jeteta1.Fill(t_decay.Jet_eta1,D_weight)
    dhist_jetphi1.Fill(t_decay.Jet_phi1,D_weight)
    dhist_jetpt2.Fill(t_decay.Jet_pt2,D_weight)
    dhist_jeteta2.Fill(t_decay.Jet_eta2,D_weight)
    dhist_jetphi2.Fill(t_decay.Jet_phi2,D_weight)
    dhist_met.Fill(t_decay.MEt_Et,D_weight)
    dhist_mphi.Fill(t_decay.MEt_Phi,D_weight)



rf1 = ROOT.TFile("input_plot_delphes_jeteta2.root","Recreate")
rf1.cd()

c1 = ROOT.TCanvas()

hist_pt1.SetLineColor(2)
hist_eta1.SetLineColor(2)
hist_phi1.SetLineColor(2)
hist_pt2.SetLineColor(2)
hist_eta2.SetLineColor(2)
hist_phi2.SetLineColor(2)
hist_jetpt1.SetLineColor(2)
hist_jeteta1.SetLineColor(2)
hist_jetphi1.SetLineColor(2)
hist_jetpt2.SetLineColor(2)
hist_jeteta2.SetLineColor(2)
hist_jetphi2.SetLineColor(2)
hist_met.SetLineColor(2)
hist_mphi.SetLineColor(2)


dhist_pt1.SetLineColor(1)
dhist_eta1.SetLineColor(1)
dhist_phi1.SetLineColor(1)
dhist_pt2.SetLineColor(1)
dhist_eta2.SetLineColor(1)
dhist_phi2.SetLineColor(1)
dhist_jetpt1.SetLineColor(1)
dhist_jeteta1.SetLineColor(1)
dhist_jetphi1.SetLineColor(1)
dhist_jetpt2.SetLineColor(1)
dhist_jeteta2.SetLineColor(1)
dhist_jetphi2.SetLineColor(1)
dhist_met.SetLineColor(1)
dhist_mphi.SetLineColor(1)


#hist_pt1.Draw()
#hist_eta1.Draw()
#hist_phi1.Draw()
#hist_pt2.Draw()
#hist_eta2.Draw()
#hist_phi2.Draw()
#hist_jetpt1.Draw()
#hist_jeteta1.Draw()
#hist_jetphi1.Draw()
#hist_jetpt2.Draw()
hist_jeteta2.Draw()
#hist_jetphi2.Draw()
#hist_met.Draw()
#hist_mphi.Draw()


#dhist_pt1.Draw("same")
#dhist_eta1.Draw("same")
#dhist_phi1.Draw()
#dhist_pt2.Draw("same")
#dhist_eta2.Draw("same")
#dhist_phi2.Draw()
#dhist_jetpt1.Draw("same")
#dhist_jeteta1.Draw("same")
#dhist_jetphi1.Draw()
#dhist_jetpt2.Draw("same")
dhist_jeteta2.Draw("same")
#dhist_jetphi2.Draw()
#dhist_met.Draw()
#dhist_mphi.Draw()

leg = ROOT.TLegend(0.1,0.1,0.2,0.2)
leg.AddEntry("ha", "non_decay")
leg.AddEntry("things", "decay")
leg.Draw()


print "Non decay integral:", hist_pt1.Integral()
print "Decay integral:", dhist_pt1.Integral()
print "Difference (decay - notdecay):", dhist_pt1.Integral()-hist_pt1.Integral()


c1.Write()

rf1.Write();rf1.Close()
