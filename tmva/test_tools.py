import ROOT
import pdb
import math

def CalcE(hist):
    e=0
    hist.Scale(1./hist.GetSum())
    for i in range(1,hist.GetNbinsX()+1):
        e+=-1*hist.GetBinContent(i)*math.log(hist.GetBinContent(i),2)
    return e
def CalcI(func,tree,n_bins=1000):
    join_d=[]#ROOT.TH2F("joint",0,25,)
    tar_d=[]#ROOT.TH1F("tar",0.25)
    test_d=[]#ROOT.TH1F("test",0,25) 
    for evt in range(tree.GetEntries()):
        tree.GetEntry(evt)
        v=func(tree)
        join_d.append([v,tree.target])
        tar_d.append(tree.target)
        test_d.append(v)
    state=0
    state_d={}
    for i in set(tar_d):
        state_d[i]=state
        state+=1
    
    tar_max= max(state_d.values())
    test_min=min(test_d)
    test_max=max(test_d)

        
    tar_h=ROOT.TH1F("Target","Target",tar_max,0,tar_max)
    test_h=ROOT.TH1F("Test_h","Test_h",n_bins,test_min,test_max)
    join_h=ROOT.TH2F("TT","TT",tar_max,0,tar_max,n_bins,test_min,test_max)
    [tar_h.Fill(state_d[i]) for i in tar_d] 
    [test_h.Fill(i) for i in test_d] 
    [join_h.Fill(state_d[i],n) for n,i in join_d] 
#    pdb.set_trace()
    join_h.Scale(1/join_h.GetSum()) #max these probs
    test_h.Scale(1/test_h.GetSum())
    tar_h.Scale(1/tar_h.GetSum())

 #   print test_min,test_max

    I=0
    for x in range(1,tar_max+1): 
        for y in range(1,n_bins+1):
            if test_h.GetBinContent(y)*tar_h.GetBinContent(x)==0 or join_h.GetBinContent(x,y)==0:  continue
            I+= join_h.GetBinContent(x,y)*math.log(join_h.GetBinContent(x,y)/(test_h.GetBinContent(y)*tar_h.GetBinContent(x)),2)

    return I,test_h,tar_h,join_h

def GetLs(tree):
    l1=ROOT.TLorentzVector()
    l1.SetPtEtaPhiM(tree.Lep_pt1,tree.Lep_eta1,tree.Lep_phi1,0)
    l2=ROOT.TLorentzVector()
    l2.SetPtEtaPhiM(tree.Lep_pt2,tree.Lep_eta2,tree.Lep_phi2,0)
    return l1,l2


def LepPt1(tree):
    return tree.Lep_pt1

def dPhi(tree):
    l1,l2=GetLs(tree)
    return l1.DeltaPhi(l2)



t=ROOT.TFile("Output.root")
tree=t.Get("Test")

I,test,tar,join=CalcI(dPhi,tree,10)
print CalcE(tar),I
print I/CalcE(tar)
