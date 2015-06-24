import pystyle
import ROOT
wz_rf=ROOT.TFile("templates/WZ_bkg.root")
ww_rf=ROOT.TFile("templates/parton.root")

wz_data=wz_rf.Get("norm")
ww_data=ww_rf.Get("norm")
ww_OO=ww_rf.Get("OOw")

ww_LL=ww_rf.Get("LLw")
ww_RR=ww_rf.Get("RRw")


for h in [wz_data,ww_data,ww_OO,ww_LL,ww_RR]:
    h.Scale(1./h.Integral())
ww_data.SetLineColor(ROOT.kRed)
ww_OO.SetLineColor(ROOT.kGreen)

ww_LL.SetLineColor(ROOT.kBlack)
ww_RR.SetLineColor(ROOT.kViolet)

c1=ROOT.TCanvas()
h=wz_data.ProjectionX("wzx",0,1000)
h.SetXTitle("1-D projection of NN output ")
h.SetYTitle("A.U.")
h.Draw("")
h1=ww_data.ProjectionX("wwx",0,10000)
h1.Draw("same")
#ww_OO.ProjectionX("wOO",0,10000).Draw("same")
#ww_LL.ProjectionX("wLL",0,10000).Draw("same")
h2=ww_RR.ProjectionX("wRR",0,10000)
h2.Draw("same")

leg=ROOT.TLegend(0.3,0.6,0.5,0.8)
leg.SetLineWidth(0)
leg.SetLineColor(ROOT.kWhite)
leg.SetFillColor(ROOT.kWhite)
leg.AddEntry(h,"WZ background shape")
leg.AddEntry(h1,"WW All SM")
leg.AddEntry(h2,"WW Right-Right tempate")
leg.Draw()
