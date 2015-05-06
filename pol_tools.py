import ROOT
import math

"""Some convient functions for calcualting cos theta star, and boosting to correct frames"""


def GetL4M(t,index):
    x=ROOT.TLorentzVector()
    x.SetPxPyPzE(t.p_px[index],t.p_py[index],t.p_pz[index],t.p_E[index])
    return x

def Get4Vects(t):
    W1l=None
    W1n=None
    W2l=None
    W2n=None
    jets=[]
    for i,p in enumerate(t.p_id):                
        if abs(p)in [11,13,15]:
            if W1l==None:
                W1l=i
            elif W2l==None:
                W2l=i
        elif abs(p) in [12,14,16]:
            if W1n==None:
                W1n=i
            elif W2n==None:
                W2n=i
        elif abs(p) in [1,2,3,4,5]:
            if t.p_status[i]==1:
                jets.append(GetL4M(t,i))
    if t.p_mother1[W1l]==t.p_mother1[W1n]:
        W1=[GetL4M(t,W1l),GetL4M(t,W1n)]
        W2=[GetL4M(t,W2l),GetL4M(t,W2n)]
    else:
        W1=[GetL4M(t,W1l),GetL4M(t,W2n)]
        W2=[GetL4M(t,W2l),GetL4M(t,W1n)]
    if len(jets)!= 2:return W1,W2
    return W1,W2,jets[0],jets[1]

def Boost_evt_rest(four_vs):
    B=four_vs[0].Clone()
    for v in four_vs[1:]:
        B+=v
    for v in four_vs:
        v.Boost(-B.BoostVector())

def Boost_to_rest(W1):
    l1,l2=W1
    Wv=l1+l2
    l1.Boost( -Wv.BoostVector() )
    l2.Boost( -Wv.BoostVector() )
    return [l1,l2,Wv]

def GetCosThetaS(W1):
    l,n,Wv=Boost_to_rest(W1)
    return math.cos(Wv.Angle(l.Vect()))
