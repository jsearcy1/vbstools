import ROOT
import sys
import pdb

class p_ratio:
    def __init__(self):
        self.bins=[40,0,20]
    def var(self,t):
        return t.Lep_pt1/t.Jet_pt1*t.Lep_pt2/t.Jet_pt2

class lep_ratio:
    def __init__(self):
        self.bins=[40,1,10]
    def var(self,t):
        if t.Lep_pt1 > t.Lep_pt2 : return t.Lep_pt1/t.Lep_pt2
        else:return t.Lep_pt1/t.Lep_pt2

class cts1:
    def __init__(self):
        self.bins=[30,-1,1]
    def var(self,t):
        return t.ct1 

class LepDPhi:
    def __init__(self):
        self.bins=[30,0,3.1415]
    def var(self,t):
        return abs(t.Lep_phi1-t.Lep_phi2) 
class LepDEta:
    def __init__(self):
        self.bins=[30,0,10]
    def var(self,t):
        return abs(t.Lep_eta1-t.Lep_eta2) 


def SetColorD(hist_d,fill=False):
    hist_d["oo"].SetLineColor(ROOT.kRed)
    hist_d["ol"].SetLineColor(ROOT.kRed+1)
    hist_d["or"].SetLineColor(ROOT.kRed+2)
    hist_d["ll"].SetLineColor(ROOT.kBlue)
    hist_d["rr"].SetLineColor(ROOT.kBlue+2)
    hist_d["lr"].SetLineColor(ROOT.kBlue+1)
    
    hist_d["oo"].SetMarkerColor(ROOT.kRed)
    hist_d["ol"].SetMarkerColor(ROOT.kRed+1)
    hist_d["or"].SetMarkerColor(ROOT.kRed+2)
    hist_d["ll"].SetMarkerColor(ROOT.kBlue)
    hist_d["rr"].SetMarkerColor(ROOT.kBlue+2)
    hist_d["lr"].SetMarkerColor(ROOT.kBlue+1)
    if fill:
        hist_d["oo"].SetFillColor(ROOT.kRed)
        hist_d["ol"].SetFillColor(ROOT.kRed+1)
        hist_d["or"].SetFillColor(ROOT.kRed+2)
        hist_d["ll"].SetFillColor(ROOT.kBlue)
        hist_d["rr"].SetFillColor(ROOT.kBlue+2)
        hist_d["lr"].SetFillColor(ROOT.kBlue+1)
    
def GetLeg(hist_d):
    leg=ROOT.TLegend(0.6,0.6,0.8,0.8)
    for h in hist_d:
        leg.AddEntry(hist_d[h],h)
    leg.SetLineColor(ROOT.kWhite)
    leg.SetFillColor(ROOT.kWhite)
    return leg

def DrawNormD(hist_d):
    c1=ROOT.TCanvas()
    SetColorD(hist_d)
    hist_d["oo"].DrawNormalized()
    hist_d["ol"].DrawNormalized("same")
    hist_d["or"].DrawNormalized("same")
    hist_d["ll"].DrawNormalized("same")
    hist_d["rr"].DrawNormalized("same")
    hist_d["lr"].DrawNormalized("same") 
    leg=GetLeg(hist_d)
    leg.Draw()

    pdb.set_trace()
    return c1

def DrawStack(hist_d):
    c1=ROOT.TCanvas()
    SetColorD(hist_d,True)
    s=ROOT.THStack("n","n")
    [s.Add(hist_d[h]) for h in ["lr","ll","rr","ol","or","oo"]]    

    leg=GetLeg(hist_d)
    s.Draw()
    leg.Draw()
    pdb.set_trace()
    return c1



func=lep_ratio()
     
def make_hists(index,bin_arr):
    bins=bin_arr[0]
    start=bin_arr[1]
    end=bin_arr[2]
    hist_oo=ROOT.TH1F("oo"+str(index),"oo"+str(index),bins,start,end)
    hist_ol=ROOT.TH1F("ol"+str(index),"ol"+str(index),bins,start,end)
    hist_or=ROOT.TH1F("or"+str(index),"or"+str(index),bins,start,end)
    hist_rr=ROOT.TH1F("rr"+str(index),"rr"+str(index),bins,start,end)
    hist_ll=ROOT.TH1F("ll"+str(index),"ll"+str(index),bins,start,end)
    hist_lr=ROOT.TH1F("lr"+str(index),"lr"+str(index),bins,start,end)
 

    hist_d={"oo":hist_oo,
            "ol":hist_ol,
            "or":hist_or,
            "ll":hist_ll,
            "rr":hist_rr,
            "lr":hist_lr
            }
    return hist_d
def FillD(t,hist_d,var):
    hist_d["oo"].Fill(var,t.OOw)
    hist_d["ol"].Fill(var,t.OLw)
    hist_d["or"].Fill(var,t.ORw)
    hist_d["ll"].Fill(var,t.LLw)
    hist_d["rr"].Fill(var,t.RRw)
    hist_d["lr"].Fill(var,t.LRw)


rf_files=sys.argv[1].split(",")



hh=[]



for i,f in enumerate(rf_files):
    rf=ROOT.TFile(f)
    t=rf.Get("Test")
    hist_d=make_hists(i,func.bins)
    hh.append(hist_d)

    for evt in range(t.GetEntries()):
        t.GetEntry(evt)
        FillD(t,hh[i],func.var(t))
        

c1=DrawNormD(hh[0])
