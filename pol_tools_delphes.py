import ROOT
import math
from itertools import product
import pdb
"""Some convient functions for calcualting cos theta star, and boosting to correct frames"""


def GetL4M(t,index):
    x=ROOT.TLorentzVector()
    x.SetPxPyPzE(t.p_px[index],t.p_py[index],t.p_pz[index],t.p_E[index])
    return x

def Get4Vects(t):
    truth_p=[p for p in t.Particle if p.Status==3] #intial born level particles
    parts={}

    for p in truth_p:   
        if parts.has_key(p.PID):
            parts[p.PID].append(p)
        else:
            parts[p.PID]=[p]
    wp_can=[]
    wm_can=[]
    ##Get all combinations of leptons and neutrions that make sense
    if parts.has_key(-11): wp_can+=product(parts[-11],parts[12])
    if parts.has_key(11):  wm_can+=product(parts[11],parts[-12])

    if parts.has_key(-13): wp_can+=product(parts[-13],parts[14])
    if parts.has_key(13): wm_can+=product(parts[13],parts[-14])

    if parts.has_key(-15): wp_can+=product(parts[-15],parts[16])
    if parts.has_key(15): wm_can+=product(parts[15],parts[-16])
    ws=[]
    # this loops over truth W's and takes the neutrio/lepton pair closest to the W four vector 
    if parts.has_key(24):
        for wp in parts[24]:
            ws.append(   min( [  [(wp.P4()-(c[0].P4()+c[1].P4())).Mag(),[c[0].P4(),c[1].P4()]] for c in wp_can ])[1] )
    if parts.has_key(-24):
        for wm in parts[-24]:
            ws.append(   min( [  [(wm.P4()-(c[0].P4()+c[1].P4())).Mag(),[c[0].P4(),c[1].P4()]] for c in wm_can ])[1] )
    
    if len(ws)!=2:
        print "dang"
        pdb.set_trace()
    W1=ws[0]
    W2=ws[1]
    return W1,W2

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
