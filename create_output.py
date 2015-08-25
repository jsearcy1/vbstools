import ROOT
from array import array
import sys
from pol_tools import *

help_str=""" 
    Usage: python create_ouput.py in_file.root out_file.root
    Script which reads the ouput of Convert.C and calculates cosTheta*
    and event weights for polarizzation
"""

class weight:
    def __init__(self):
        pass
#        self.w_rf=ROOT.TFile("./data/hists_sm.root")
#        self.f0_w=self.w_rf.Get("fo")
#        self.fl_w=self.w_rf.Get("fl")
#        self.fr_w=self.w_rf.Get("fr")


    def get_weight(self,ct1,ct2,Mww):

        ###This part is turned off right now which I think means you can't trust the normalization
#        Nbins=self.fl_w.GetNbinsX()
#        bin_n=self.fl_w.FindBin(Mww)
#        if bin_n > Nbins:bin_n=Nbins #oveflow protection
        #all histograms need the same binning
#        f0=self.f0_w.GetBinContent(bin_n)
#        fl=self.fl_w.GetBinContent(bin_n)
#        fr=self.fr_w.GetBinContent(bin_n)
#        ###        
        fr=fl=f0=1.
        norm= (  ( fr*(3./8.*(1-ct1)**2) +fl*(3./8.*(1+ct1)**2)+f0*(3./4.*(1-ct1**2))  )
                 * (  fr*(3./8.*(1-ct2)**2) +fl*(3./8.*(1+ct2)**2)+ f0*(3./4.*(1-ct2**2))  ) )
        if norm==0: 
            print "normalization is 0 this should never happen, dumping to debug shell"
            pdb.set_trace() 
        OO =( 3./4.*(1-ct1**2) )*( 3./4.*(1-ct2**2) ) 
        LL=(3./8.*(1-ct1)**2)*(3./8.*(1-ct2)**2)
        RR=(3./8.*(1+ct1)**2)*(3./8.*(1+ct2)**2)
        LR=(3./8.*(1-ct1)**2+3./8.*(1+ct1)**2)*(3./8.*(1-ct2)**2 +3./8.*(1+ct2)**2)-LL-RR
        OL=(3./8.*(1-ct1)**2)*(3./4.*(1-ct2**2))+(3./4.*(1-ct1**2))*(3./8.*(1-ct2)**2)
        OR=(3./8.*(1+ct1)**2)*(3./4.*(1-ct2**2))+(3./4.*(1-ct1**2))*(3./8.*(1+ct2)**2)
        TT=(3./8.*(1-ct1)**2+3./8.*(1+ct1)**2)*(3./8.*(1-ct2)**2 +3./8.*(1+ct2)**2)
        TO=(3./8.*(1-ct1)**2+3./8.*(1+ct1)**2)*(3./4.*(1-ct2**2))+(3./8.*(1-ct2)**2 +3./8.*(1+ct2)**2)*(3./4.*(1-ct1**2))
        return OO/norm,TT/norm,TO/norm,LL/norm,RR/norm,LR/norm,OL/norm,OR/norm

def BuildTree(tree_name,rf):
    Lep_pt1=array("f",[0.])
    Lep_eta1=array("f",[0.])
    Lep_phi1=array("f",[0.])
    Lep_charge1=array("f",[0.])

    Lep_pt2=array("f",[0.])
    Lep_eta2=array("f",[0.])
    Lep_phi2=array("f",[0.])
    Lep_charge2=array("f",[0.])


    Nu_pt1=array("f",[0.])
    Nu_eta1=array("f",[0.])
    Nu_phi1=array("f",[0.])

    Nu_pt2=array("f",[0.])
    Nu_eta2=array("f",[0.])
    Nu_phi2=array("f",[0.])

    Jet_pt1=array("f",[0.])
    Jet_eta1=array("f",[0.])
    Jet_phi1=array("f",[0.])
    Jet_m1=array("f",[0.])

    Jet_pt2=array("f",[0.])
    Jet_eta2=array("f",[0.])
    Jet_phi2=array("f",[0.])
    Jet_m2=array("f",[0.])

    Jet_pt3=array("f",[0.])
    Jet_eta3=array("f",[0.])
    Jet_phi3=array("f",[0.])
    Jet_m3=array("f",[0.])

    MEt_Et=array("f",[0.])
    MEt_Phi=array("f",[0.])

    OOw=array("f",[0.])
    TTw=array("f",[0.])
    TOw=array("f",[0.])
    LLw=array("f",[0.])
    RRw=array("f",[0.])
    LRw=array("f",[0.])
    OLw=array("f",[0.])
    ORw=array("f",[0.])


    ct1=array("f",[0.])
    ct2=array("f",[0.])
    Mww=array("f",[0.])
    


    rf.cd()       
    tree=ROOT.TTree(tree_name,tree_name)
    
    tree.Branch("Lep_pt1",Lep_pt1,"Lep_pt1/F")
    tree.Branch("Lep_eta1",Lep_eta1,"Lep_eta1/F")
    tree.Branch("Lep_phi1",Lep_phi1,"Lep_phi1/F")    
    tree.Branch("Lep_charge1",Lep_charge1,"Lep_charge1/F")    
    
    tree.Branch("Lep_pt2",Lep_pt2,"Lep_pt2/F")
    tree.Branch("Lep_eta2",Lep_eta2,"Lep_eta2/F")
    tree.Branch("Lep_phi2",Lep_phi2,"Lep_phi2/F")
    tree.Branch("Lep_charge2",Lep_charge2,"Lep_charge2/F")    
    
    tree.Branch("Nu_pt1",Nu_pt1,"Nu_pt1/F")
    tree.Branch("Nu_eta1",Nu_eta1,"Nu_eta1/F")
    tree.Branch("Nu_phi1",Nu_phi1,"Nu_phi1/F")    
    
    tree.Branch("Nu_pt2",Nu_pt2,"Nu_pt2/F")
    tree.Branch("Nu_eta2",Nu_eta2,"Nu_eta2/F")
    tree.Branch("Nu_phi2",Nu_phi2,"Nu_phi2/F")
    
    
    tree.Branch("Jet_pt1",Jet_pt1,"Jet_pt1/F")
    tree.Branch("Jet_eta1",Jet_eta1,"Jet_eta1/F")
    tree.Branch("Jet_phi1",Jet_phi1,"Jet_phi1/F")    
    tree.Branch("Jet_m1",Jet_m1,"Jet_m1/F")    
    
    tree.Branch("Jet_pt2",Jet_pt2,"Jet_pt2/F")
    tree.Branch("Jet_eta2",Jet_eta2,"Jet_eta2/F")
    tree.Branch("Jet_phi2",Jet_phi2,"Jet_phi2/F")
    tree.Branch("Jet_m2",Jet_m2,"Jet_m2/F")

    tree.Branch("Jet_pt3",Jet_pt3,"Jet_pt3/F")
    tree.Branch("Jet_eta3",Jet_eta3,"Jet_eta3/F")
    tree.Branch("Jet_phi3",Jet_phi3,"Jet_phi3/F")
    tree.Branch("Jet_m3",Jet_m3,"Jet_m3/F")
    
    tree.Branch("MEt_Et",MEt_Et,"MEt_Et/F")
    tree.Branch("MEt_Phi",MEt_Phi,"MEt_Phi/F")
    
    tree.Branch("OOw",OOw,"OOw/F")
    tree.Branch("TTw",TTw,"TTw/F") 
    tree.Branch("TOw",TOw,"TOw/F") 

    tree.Branch("LLw",LLw,"LLw/F")
    tree.Branch("RRw",RRw,"RRw/F") 
    tree.Branch("LRw",LRw,"LRw/F") 
    
    tree.Branch("OLw",OLw,"OLw/F")
    tree.Branch("ORw",ORw,"ORw/F") 
    
    tree.Branch("ct1",ct1,"ct1/F")
    tree.Branch("ct2",ct2,"ct2/F")
    tree.Branch("Mww",Mww,"Mww/F")

    var_dict={}
    for i in list(locals()):
        if type(locals()[i])==array:
            var_dict[i]=locals()[i]
    return tree,var_dict

        


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print help_str
        sys.exit()
    rf=ROOT.TFile(sys.argv[1])
    print "Output:", sys.argv[2]
    
    w_tool=weight()

    tree=rf.Get("truth")

    rf_o=ROOT.TFile(sys.argv[2],"Recreate")

    tt,var_dict=BuildTree("Test",rf_o)
    for i in var_dict:
        exec i+"="+"var_dict['"+i+"']"


    for evt in range(tree.GetEntries()):
        tree.GetEntry(evt)
        if evt%1000==0:print "Processed ",evt," events"
        four_vs=Get4Vects(tree)
        if len(four_vs)==6:
            W1,W2,j1,j2,p1,p2=Get4Vects(tree)
            
            if p1 > 0 and p2 >0:
                charge=-1
            elif p1 < 0 and p2 <0:
                charge=1
            else:
                charge=0
            skip_truth=False
            if -1 in [W1,W2,j1,j2]: continue
            l1,n1=W1
            l2,n2=W2
            MET=(n1+n2)
            MET.SetPz(0)
        if len(four_vs)==5:
            skip_truth=True
            l1,l2,nus,j1,j2=four_vs
            MET=nus[0]
            for nu in nus[1:]:
                MET=MET+nu
            n1=ROOT.TLorentzVector()
            n2=ROOT.TLorentzVector()
            charge=0
        Lep_pt1[0]=l1.Pt()
        Lep_eta1[0]=l1.Eta()
        Lep_phi1[0]=l1.Phi()
        Lep_charge1[0]=charge

        Lep_pt2[0]=l2.Pt()
        Lep_eta2[0]=l2.Eta()
        Lep_phi2[0]=l2.Phi()
        Lep_charge2[0]=charge

        if skip_truth:
            Nu_pt1[0]=0.0
            Nu_eta1[0]=0.0
            Nu_phi1[0]=0.0           
            Nu_pt2[0]=0.0
            Nu_eta2[0]=0.0
            Nu_phi2[0]=0.0
        else:
            Nu_pt1[0]=n1.Pt()
            Nu_eta1[0]=n1.Eta()
            Nu_phi1[0]=n1.Phi()
            Nu_pt2[0]=n2.Pt()
            Nu_eta2[0]=n2.Eta()
            Nu_phi2[0]=n2.Phi()


        Jet_pt1[0]=j1.Pt()
        Jet_eta1[0]=j1.Eta()
        Jet_phi1[0]=j1.Phi()

        Jet_pt2[0]=j2.Pt()
        Jet_eta2[0]=j2.Eta()
        Jet_phi2[0]=j2.Phi()

        #Jet_pt3[0]=j3.Pt()
        #Jet_eta3[0]=j3.Eta()
        #Jet_phi3[0]=j3.Phi()

        MEt_Et[0]=MET.Pt()
        MEt_Phi[0]=MET.Phi()
        
        Mww[0]=(l1+l2+n1+n2).M()
        ###Don't fill any kinematics after this, as it boosts to the rest frame!!!!
        if skip_truth:
            c1=0
            c2=0
        else:
            c1=GetCosThetaS(W2)
            c2=GetCosThetaS(W1)
            
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
    ### Write Output
    rf_o.Write()
    rf_o.Close()
