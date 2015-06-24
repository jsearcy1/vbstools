import ROOT
import sys
import pystyle
from tests.test_templates import unfold


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

h_TT=h_LL.Clone()
h_TT.Add(h_RR)
h_TT.Add(h_LR)

h_OT=h_OL.Clone()
h_OT.Add(h_OR)

h_TT.SetName("Transverse-Transverse")
h_OT.SetName("Transverse-Longitudinal")
h_OO.SetName("Longitudinal-Longitudinal")

h_TT.SetTitle("Transverse-Transverse")
h_OT.SetTitle("Transverse-Longitudinal")
h_OO.SetTitle("Longitudinal-Longitudinal")


if type(h_TT)!=ROOT.TH1F:

    c1=ROOT.TCanvas("C1","c1",1800,600)
    p1=ROOT.TPad("1","1",0,0,.33,1)
    p2=ROOT.TPad("2","2",.33,0,.66,1)
    p3=ROOT.TPad("3","3",.66,0,1,1)
#p4=ROOT.TPad("4","4",0,0.5,.33,1)
#p5=ROOT.TPad("5","5",.33,0.5,.66,1)
#p6=ROOT.TPad("6","6",.66,0.5,1,1)
    pads=[p1,p2,p3]
    [p.Draw() for p in pads]

    for h,p in zip([h_TT,h_OT,h_OO],pads):
        p.cd()
        h.Scale(1./h.Integral(0,1000,0,1000))
        h.GetXaxis().SetTitleOffset(1.25)
        h.GetYaxis().SetTitleOffset(1.25)
        h.SetMaximum(0.03)
        h.SetMinimum(0.00)
        h.SetXTitle("Predicted cos(#theta*_{1})")
        h.SetYTitle("Predicted cos(#theta*_{2})")
        h.DrawNormalized("col")
    c1.SaveAs("plots/templates_2D.pdf")
    c1.SaveAs("plots/templates_2D.root")
else:
    c2=ROOT.TCanvas()
    c2.cd()
    h_TT.SetLineColor(pystyle.colors[0])
    h_OT.SetLineColor(pystyle.colors[1])
    h_OT.SetLineColor(pystyle.colors[2])

    h_TT.SetLineWidth(3)
    h_OT.SetLineWidth(3)
    h_OO.SetLineWidth(3)


    leg=ROOT.TLegend(0.5,0.5,0.89,0.89)
    leg.SetLineColor(ROOT.kWhite)
    leg.SetFillColor(ROOT.kWhite)
    leg.AddEntry(h_TT,"Transverse-Transverse")
    leg.AddEntry(h_OT,"Transverse-Longitudinal")
    leg.AddEntry(h_OO,"Longitudinal-Longitudinal")
    h_TT.SetXTitle("R_{pT}")
    h_TT.SetYTitle("A.U.")
    
    h_TT.DrawNormalized()
    h_OT.DrawNormalized("same")
    h_OO.DrawNormalized("same")
    c2.SetLogy()
    c2.Draw()
    leg.Draw()
    c2.SaveAs("plots/templates_2D.pdf")
    c2.SaveAs("plots/templates_2D.root")
