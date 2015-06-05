import ROOT
from array import array
import sys
from pol_tools_delphes import *
from create_output import weight, BuildTree

help_str=""" 
    Usage: python create_ouput.py in_file.root out_file.root xsec_in_fb
    Script which reads the ouput of Convert.C and calculates cosTheta*
    and event weights for polarization input is from delphes output
"""
        

class delphes_evt:
    def __init__(self):
        self.jet_pt_cut=30.
        self.jet_eta_cut=4.5
        self.lep_pt_cut=20.
        self.lep_eta_cut=2.5
        self.mll_cut=20.
        self.met_cut=40.
        self.mjj_cut=500.
        self.dyjj_cut=2.4

    def load_evt(self,t):
        jets=[[j,j.P4()] for j in t.Jet if j.PT > self.jet_pt_cut and abs(j.Eta)<self.jet_eta_cut ]
        jets.sort()
        jets.reverse()
        self.jets=[j[1] for j in jets]
        self.muons=[m.P4() for m in t.Muon if m.PT > self.lep_pt_cut and abs(m.Eta)<self.lep_eta_cut ]
        self.electrons=[e.P4() for e in t.Electron if e.PT > self.lep_pt_cut and abs(e.Eta)<self.lep_eta_cut ]
        self.MET=t.MissingET[0].P4()
        self.MET.SetPz(0) #not sure why this isn't done automatically by delphes
        self.leps=self.muons+self.electrons

    def pass_cuts(self):
        if len(self.leps)!=2:return False
        if len(self.jets)<2:return False
        if self.MET.Pt()<self.met_cut:return False
        self.mjj=(self.jets[0]+self.jets[1]).M()
        if self.mjj < self.mjj_cut: return False        
        self.dyjj=abs(self.jets[0].Eta()-self.jets[1].Eta())
        if self.dyjj < self.dyjj_cut: return False
        self.mll=(self.leps[0]+sef.leps[1]).M()
        if self.mll < self.mll_cut:return False
        return True


if __name__ == "__main__":

    ROOT.gSystem.Load("/atlas/data19/jsearcy/MG5_aMC_v2_2_3/Delphes/libDelphes.so")
    
    if len(sys.argv) != 4: 
        sys.exit()
    rf=ROOT.TFile(sys.argv[1])
    
    w_tool=weight()

    tree=rf.Get("Delphes")

    rf_o=ROOT.TFile(sys.argv[2],"Recreate")

    tt,var_dict=BuildTree("Test",rf_o)

    for i in var_dict:
        exec i+"="+"var_dict['"+i+"']"
    devt=delphes_evt()
    xsec_weight=float(sys.argv[3])/tree.GetEntries()

    for evt in range(tree.GetEntries()):
        tree.GetEntry(evt)
        devt.load_evt(tree)        

        if evt%1000==0:print "Processed ",evt," events"
        W1,W2=Get4Vects(tree)
        l1,n1=W1
        l2,n2=W2
        Mww[0]=(l1+l2+n1+n2).M()

        MET=devt.MET

        if len(devt.leps) ==2:
            Lep_pt1[0]=devt.leps[0].Pt()
            Lep_eta1[0]=devt.leps[0].Eta()
            Lep_phi1[0]=devt.leps[0].Phi()
            Lep_pt2[0]=devt.leps[1].Pt()
            Lep_eta2[0]=devt.leps[1].Eta()
            Lep_phi2[0]=devt.leps[1].Phi()
        if len(devt.jets) >=2: #jets are pt sorted
            Jet_pt1[0]=devt.jets[0].Pt()
            Jet_eta1[0]=devt.jets[0].Eta()
            Jet_phi1[0]=devt.jets[0].Phi()

            Jet_pt2[0]=devt.jets[1].Pt()
            Jet_eta2[0]=devt.jets[1].Eta()
            Jet_phi2[0]=devt.jets[1].Phi()

        MEt_Et[0]=MET.Pt()
        MEt_Phi[0]=MET.Phi()
        

        ###Don't fill truth level kinematics after this, as it boosts to the rest frame!!!!
        c1=GetCosThetaS(W1)
        c2=GetCosThetaS(W2)
        ct1[0]=c1
        ct2[0]=c2

        OO,TT,TO,LL,RR,LR,OL,OR=w_tool.get_weight(c1,c2,Mww[0])

        OOw[0]=OO
        TTw[0]=TT
        TOw[0]=TO

        LLw[0]=LL
        RRw[0]=RR
        LRw[0]=LR

        OLw[0]=OL
        ORw[0]=OR
        tt.Fill()
        for i in var_dict: #rest variables
            var_dict[i][0]=0. 
    ### Write Output
    rf_o.Write()
    rf_o.Close()
