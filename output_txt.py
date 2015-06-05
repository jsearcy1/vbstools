import ROOT
import sys

input_vars=["Lep_pt1","Lep_eta1",
        "Lep_phi1","Lep_pt2",
        "Lep_eta2","Lep_phi2",
        "Jet_pt1","Jet_eta1",
        "Jet_phi1", "Jet_pt2",
        "Jet_eta2","Jet_phi2",
        "MEt_Et","MEt_Phi","Mww"]


rf=ROOT.TFile(sys.argv[1])
t=rf.Get("Test")
print ",".join(input_vars)
for i in range(t.GetEntries()):
    t.GetEntry(i)
    print ",".join([str(getattr(t,i)) for i in input_vars])
