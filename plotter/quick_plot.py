import ROOT
import sys

def p_ratio(t):
    return t.Lep_pt1/t.Jet_pt1*t.Lep_pt2/t.Jet_pt2
    

rf_files=sys.argv[1].split(",")

hist=ROOT.TH1F("n","n",20,0,20)
hh=[]

func=p_ratio
for i,f in enumerate(rf_files):
    rf=ROOT.TFile(f)
    t=rf.Get("Test")
    exec "hist"+str(i)+"=hist.Clone()"
    exec "hist"+str(i)+".SetDirectory(0)"
    exec "hh.append(hist"+str(i)+")"
    for evt in range(t.GetEntries()):
        t.GetEntry(evt)
        hh[i].Fill(func(t))



