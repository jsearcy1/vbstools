import ROOT
import sys
import pystyle


c1=ROOT.TCanvas()
rf=ROOT.TFile(sys.argv[1])

h_L=rf.Get("L")
h_R=rf.Get("R")
h_O=rf.Get("O")

h_LL=rf.Get("LLw")
h_RR=rf.Get("RRw")
h_OO=rf.Get("OOw")
h_OL=rf.Get("OLw")
h_OR=rf.Get("ORw")
h_LR=rf.Get("LRw")


c1=ROOT.TCanvas()
p1=ROOT.TPad("1","1",0,0,.33,.5)
p2=ROOT.TPad("2","2",.33,0,.66,.5)
p3=ROOT.TPad("3","3",.66,0,1,.5)
p4=ROOT.TPad("4","4",0,0.5,.33,1)
p5=ROOT.TPad("5","5",.33,0.5,.66,1)
p6=ROOT.TPad("6","6",.66,0.5,1,1)
pads=[p1,p2,p3,p4,p5,p6]
[p.Draw() for p in pads]

for h,p in zip([h_LL,h_LR,h_RR,h_OL,h_OO,h_OR],pads):
    p.cd()
    h.Draw("colz")

c2=ROOT.TCanvas()
c2.cd()
h_L.SetLineColor(pystyle.colors[0])
h_R.SetLineColor(pystyle.colors[1])
h_O.SetLineColor(pystyle.colors[2])
h_L.SetLineWidth(2)
h_R.SetLineWidth(2)
h_O.SetLineWidth(2)

h_L.DrawNormalized()
h_R.DrawNormalized("same")
h_O.DrawNormalized("same")
c2.Draw()
