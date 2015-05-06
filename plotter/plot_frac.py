import ROOT

c1=ROOT.TCanvas()
leg=ROOT.TLegend(0.6,0.6,0.8,0.8)
hists=[]
def Plot_hists(rf,color,leg,name):
    hr=rf.Get("fr")
    hl=rf.Get("fl")
    ho=rf.Get("fo")
    hr.SetMarkerStyle(22)
    hl.SetMarkerStyle(24)
    ho.SetMarkerStyle(25)

    hr.SetMarkerColor(color)
    hl.SetMarkerColor(color)
    ho.SetMarkerColor(color)

    hr.SetLineColor(color)
    hl.SetLineColor(color)
    ho.SetLineColor(color)
    
    leg.AddEntry(ho,name,"lF")
    print rf,name
    return hr,hl,ho

sm=ROOT.TFile("hists_sm.root")
sm_500=ROOT.TFile("hists_sm500.root")
thdm=ROOT.TFile("hists_2HDM.root")

[hists.append(i) for i in Plot_hists(sm,ROOT.kBlue,leg,"SM Mh=126")]
[hists.append(i) for i in Plot_hists(sm_500,ROOT.kBlack,leg,"SM Mh=500")]
[hists.append(i) for i in Plot_hists(thdm,ROOT.kRed,leg,"S2HDM Mh=125 MH=326")]


hists[0].SetMaximum(1)
hists[0].SetMinimum(0.)
hists[0].Draw()
leg.AddEntry(hists[0],"fl","P")
leg.AddEntry(hists[1],"fr","P")
leg.AddEntry(hists[2],"fo","P")

[i.Draw("same") for i in hists[1:]]


