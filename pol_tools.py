import ROOT
import math
import pdb
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
    leps=[]
    neus=[]

    for i,p in enumerate(t.p_id):                
        if t.p_px[i]==0 and t.p_py[i]==0:continue
        ## This we need to catch WZ particles
        if abs(p)in [11,13,15]:
            if W1l==None:
                W1l=i
            elif W2l==None:
                W2l=i
            leps.append([p,i])
        elif abs(p) in [12,14,16]:
            if W1n==None:
                W1n=i
            elif W2n==None:
                W2n=i
            neus.append([p,i])
        elif abs(p) in [1,2,3,4,5,21]:
            if t.p_status[i]==1:
                jets.append(GetL4M(t,i))
    if len(leps) ==0 or len(jets)!=2:
        pdb.set_trace()
        return -1
    if len(leps)==3:#IF we get WZ return two ss leptons
        neu_4v=[GetL4M(t,l[1]) for l in neus]
        if leps[0][0]*leps[1][0] > 0:
            return GetL4M(t,leps[0][1]),GetL4M(t,leps[1][1]),neu_4v,jets[0],jets[1]
        elif leps[0][0]*leps[2][0] > 0:
            return GetL4M(t,leps[0][1]),GetL4M(t,leps[2][1]),neu_4v,jets[0],jets[1]
        elif leps[1][0]*leps[2][0] > 0:
            return GetL4M(t,leps[1][1]),GetL4M(t,leps[2][1]),neu_4v,jets[0],jets[1]
        else:
            return -1
    if t.p_mother1[W1l]==t.p_mother1[W1n]:
        W1=[GetL4M(t,W1l),GetL4M(t,W1n)]
        W2=[GetL4M(t,W2l),GetL4M(t,W2n)]
    else:
        W1=[GetL4M(t,W1l),GetL4M(t,W2n)]
        W2=[GetL4M(t,W2l),GetL4M(t,W1n)]
    if len(jets)!= 2:return W1,W2
    return W1,W2,jets[0],jets[1],t.p_id[W1l],t.p_id[W2l]

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
