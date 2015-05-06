import ROOT

def GetLvect(tree):
    l1=ROOT.TLorentzVector()
    l1.SetPtEtaPhiM(tree.Lep_pt1,tree.Lep_eta1,tree.Lep_phi1,0)
    l2=ROOT.TLorentzVector()
    l2.SetPtEtaPhiM(tree.Lep_pt2,tree.Lep_eta2,tree.Lep_phi2,0)
    return l1,l2



def MakeHists(hist,func,tree): 
    TT=hist.Clone()
    TL=hist.Clone()
    LL=hist.Clone()

    for evt in range(tree.GetEntries()):
        tree.GetEntry(evt)
        v=func(tree)
        TT.Fill(v,tree.TTw)
        TL.Fill(v,tree.TLw)
        LL.Fill(v,tree.LLw)
    return TT,TL,LL

def MakePlot(TT,TL,LL):
    c1=ROOT.TCanvas()
    TT.SetLineColor(ROOT.kRed)
    TL.SetLineColor(ROOT.kBlue)
    LL.SetLineColor(ROOT.kGreen)
    leg=ROOT.TLegend(.7,.7,.9,.9)
    leg.AddEntry(TT,"TT")
    leg.AddEntry(TL,"TL")
    leg.AddEntry(LL,"LL")
    TT.DrawNormalized()
    TL.DrawNormalized("same")
    LL.DrawNormalized("same")
    leg.Draw()
    raw_input()

def Mll(tree):
    l1,l2=GetLvect(tree)
    return (l1+l2).M()
def dPhi(tree):
    l1,l2=GetLvect(tree)
    return l1.DeltaPhi(l2)
def dR(tree):
    l1,l2=GetLvect(tree)
    return l1.DeltaR(l2)
def Sum_Pt(tree):
    return tree.Lep_pt1+tree.Lep_pt2
def Sum_PtwM(tree):
    return tree.Lep_pt1+tree.Lep_pt2+tree.MEt_Et
def Lep_pt1(tree):
    return tree.Lep_pt1
def Lep_pt2(tree):
    return tree.Lep_pt2
def Lep_pt1opt2(tree):
    return tree.Lep_pt1/tree.Lep_pt2



rf=ROOT.TFile("Output.root")
tt=rf.Get("Test")

pt=ROOT.TH1F("pt","pt",20,0,1000)
p_ratio=ROOT.TH1F("pr","pt",20,0,4)
ds=ROOT.TH1F("pr","pt",20,-4,4)
mll_h=ROOT.TH1F("mll","mll",20,0,500)

for func,hist in [
    (Lep_pt1,pt),
    (Lep_pt2,pt),
    (Lep_pt1opt2,p_ratio),
    (Mll,mll_h),
    (dPhi,ds),
    (dR,ds),
    (Sum_Pt,pt),
    (Sum_PtwM,pt)
    ]:

    TT,TL,LL=MakeHists(hist,func,tt)
    MakePlot(TT,TL,LL)
