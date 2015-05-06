import ROOT
from array import array
import sys
from pol_tools import *

rf= ROOT.TFile(sys.argv[1])
print "Output:", sys.argv[2]
tree=rf.Get("truth")

m=ROOT.TH1F("M","M",50,78,82)
cost=ROOT.TH1F("cts","cts",20,-1,1)
n_x=4
n_y=4
cost2D=ROOT.TH2F("cts2","cts2",n_x,-1,1,n_y,-.8,1)

H_frac_func=ROOT.TF1("hff","[0]*3/8*((1+x^2)+1/2*[1]*(1-3*x^2)+[2]*x )",-1,1)
H_frac_func2=ROOT.TF2("hff2","[0]*9/64*((1+x^2)+1/2*[1]*(1-3*x^2)+[2]*x )*((1+y^2)+1/2*[3]*(1-3*y^2)+[4]*y ) ",-1,1)


fit_func=ROOT.TF1("cts","[0]*(3/8*(1-x)^2*[1] +3/8*(1+x)^2*[2]+3/4*(1-x^2)*[3])",-.8,1)
fit_func2=ROOT.TF2("cts2","[0]*(3/8*(1-x)^2*[1] +3/8*(1+x)^2*[2]+3/4*(1-x^2)*[3])*(3/8*(1-y)^2*[4] +3/8*(1+y)^2*[5]+3/4*(1-y^2)*[6])",-.8,1)

w_rf=ROOT.TFile("hists_sm.root")
f0_w=w_rf.Get("fo")
fl_w=w_rf.Get("fl")
fr_w=w_rf.Get("fr")

def Weight(ct1,ct2,Mww):
    Nbins=fl_w.GetNbinsX()
    bin_n=fl_w.FindBin(Mww)
    if bin_n > Nbins:bin_n=Nbins #oveflow protection
#all histograms need the same binning
    f0=f0_w.GetBinContent(bin_n)
    fl=fl_w.GetBinContent(bin_n)
    fr=fr_w.GetBinContent(bin_n)

    norm= (  ( fr*(3./8.*(1-ct1)**2) +fl*(3./8.*(1+ct1)**2)+f0*(3./4.*(1-ct1**2))  )
             * (  fr*(3./8.*(1-ct2)**2) +fl*(3./8.*(1+ct2)**2)+ f0*(3./4.*(1-ct2**2))  ) )

    if norm==0: pdb.set_trace()

    OO =( 3./4.*(1-ct1**2) )*( 3./4.*(1-ct2**2) ) 
    LL=(3./8.*(1-ct1)**2)*(3./8.*(1-ct2)**2)
    RR=(3./8.*(1+ct1)**2)*(3./8.*(1+ct2)**2)
    LR=(3./8.*(1-ct1)**2+3./8.*(1+ct1)**2)*(3./8.*(1-ct2)**2 +3./8.*(1+ct2)**2)-LL-RR
    OL=(3./8.*(1-ct1)**2)*(3./4.*(1-ct2**2))+(3./4.*(1-ct1**2))*(3./8.*(1-ct2)**2)
    OR=(3./8.*(1+ct1)**2)*(3./4.*(1-ct2**2))+(3./4.*(1-ct1**2))*(3./8.*(1+ct2)**2)
    TT=(3./8.*(1-ct1)**2+3./8.*(1+ct1)**2)*(3./8.*(1-ct2)**2 +3./8.*(1+ct2)**2)
    TO=(3./8.*(1-ct1)**2+3./8.*(1+ct1)**2)*(3./4.*(1-ct2**2))+(3./8.*(1-ct2)**2 +3./8.*(1+ct2)**2)*(3./4.*(1-ct1**2))
    return OO/norm,TT/norm,TO/norm,LL/norm,RR/norm,LR/norm,OL/norm,OR/norm
    



fl=ROOT.TF1("fl","[0]*(3/8*(1-x)^2*[1])",-1,1)
fr=ROOT.TF1("fr","[0]*(3/8*(1+x)^2*[1])",-1,1)
f0=ROOT.TF1("f0","[0]*(3/4*(1-x^2)*[1])",-1,1)

Lep_pt1=array("f",[0.])
Lep_eta1=array("f",[0.])
Lep_phi1=array("f",[0.])
#Lep_charge1=array("f",[0.])

Lep_pt2=array("f",[0.])
Lep_eta2=array("f",[0.])
Lep_phi2=array("f",[0.])
#Lep_charge2=array("f",[0.])


Nu_pt1=array("f",[0.])
Nu_eta1=array("f",[0.])
Nu_phi1=array("f",[0.])
#Nu_charge1=array("f",[0.])

Nu_pt2=array("f",[0.])
Nu_eta2=array("f",[0.])
Nu_phi2=array("f",[0.])
#Nu_charge2=array("f",[0.])


Jet_pt1=array("f",[0.])
Jet_eta1=array("f",[0.])
Jet_phi1=array("f",[0.])
#Jet_charge1=array("f",[0.])

Jet_pt2=array("f",[0.])
Jet_eta2=array("f",[0.])
Jet_phi2=array("f",[0.])
#Lep_charge2=array("f",[0.])


target=array("f",[0.])
MEt_Et=array("f",[0.])
MEt_Phi=array("f",[0.])
#MEt_Ex=array("f",[0.])
#MEt_Ey=array("f",[0.])
#Mjj=array("f",[0.])
 
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


rf_o=ROOT.TFile(sys.argv[2],"Recreate")

def BuildTree(tree_name,rf):
    rf.cd()       
    tree=ROOT.TTree(tree_name,tree_name)
    
    tree.Branch("Lep_pt1",Lep_pt1,"Lep_pt1/F")
    tree.Branch("Lep_eta1",Lep_eta1,"Lep_eta1/F")
    tree.Branch("Lep_phi1",Lep_phi1,"Lep_phi1/F")    
    tree.Branch("Lep_pt2",Lep_pt2,"Lep_pt2/F")
    tree.Branch("Lep_eta2",Lep_eta2,"Lep_eta2/F")
    tree.Branch("Lep_phi2",Lep_phi2,"Lep_phi2/F")

    tree.Branch("Nu_pt1",Nu_pt1,"Nu_pt1/F")
    tree.Branch("Nu_eta1",Nu_eta1,"Nu_eta1/F")
    tree.Branch("Nu_phi1",Nu_phi1,"Nu_phi1/F")    
    tree.Branch("Nu_pt2",Nu_pt2,"Nu_pt2/F")
    tree.Branch("Nu_eta2",Nu_eta2,"Nu_eta2/F")
    tree.Branch("Nu_phi2",Nu_phi2,"Nu_phi2/F")

   
    tree.Branch("Jet_pt1",Jet_pt1,"Jet_pt1/F")
    tree.Branch("Jet_eta1",Jet_eta1,"Jet_eta1/F")
    tree.Branch("Jet_phi1",Jet_phi1,"Jet_phi1/F")    
    tree.Branch("Jet_pt2",Jet_pt2,"Jet_pt2/F")
    tree.Branch("Jet_eta2",Jet_eta2,"Jet_eta2/F")
    tree.Branch("Jet_phi2",Jet_phi2,"Jet_phi2/F")
    
    tree.Branch("target",target,"target/F")    
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


    return tree

    return LL/norm,TT/norm,TL/norm


names=["Lep_pt1","Lep_eta1","Lep_phi1","Lep_pt2","Lep_eta2","Lep_phi2","target"]#,"MET_Et","MET_Phi"]
nbins=array("i",[3  ,3   ,3    ,3 ,3   ,3    ,(n_x+2)*(n_y+2)])#,5  ,3    ])
xmin=array("d", [0  ,-2.5,-3.146,0  ,-2.5,-3.146,0           ])#   ,0  ,-3.146])
xmax=array("d", [100,2.5 ,3.146 ,100,2.5 ,3.146 ,(n_x+2)*(n_y+2)])#,100,3.146])

b_h=ROOT.THnSparseF("Big_h","Big_h",len(nbins),nbins,xmin,xmax)
for i,n in enumerate(names):
    b_h.GetAxis(i).SetNameTitle(n,n)

tt=BuildTree("Test",rf_o)


fit_func.SetParameter(0,cost.Integral())
fit_func.SetParameter(1,.33)
fit_func.SetParameter(2,.33)
fit_func.SetParameter(3,.33)

fit_func2.SetParameter(0,cost.Integral())
fit_func2.SetParameter(1,.33)
fit_func2.SetParameter(2,.33)
fit_func2.SetParameter(3,.33)
fit_func2.SetParameter(4,.33)
fit_func2.SetParameter(5,.33)
fit_func2.SetParameter(6,.33)


#for evt in range(100):
for evt in range(tree.GetEntries()):
    tree.GetEntry(evt)
    if evt%1000==0:print evt
    W1,W2,j1,j2=Get4Vects(tree)
#    Boost_evt_rest(W1+W2+[j1]+[j2])

    if -1 in [W1,W2,j1,j2]: continue
    l1,n1=W1
    l2,n2=W2
    MET=(n1+n2)
    MET.SetPz(0)

    m.Fill((W1[0]+W1[1]).M())
    m.Fill((W2[0]+W2[1]).M())


  
    Lep_pt1[0]=l1.Pt()
    Lep_eta1[0]=l1.Eta()
    Lep_phi1[0]=l1.Phi()

    Lep_pt2[0]=l2.Pt()
    Lep_eta2[0]=l2.Eta()
    Lep_phi2[0]=l2.Phi()

  
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


    
    MEt_Et[0]=MET.Pt()
    MEt_Phi[0]=MET.Phi()
    Mww[0]=(l1+l2+n1+n2).M()


    c1=GetCosThetaS(W2)
    c2=GetCosThetaS(W1)
    ct1[0]=c1
    ct2[0]=c2
    cost.Fill(c1)
    cost.Fill(c2)
    cost2D.Fill(c1,c2) # Should we sort c1 c2?
    
    OO,TT,TO,LL,RR,LR,OL,OR=Weight(c1,c2,Mww[0])
 
    
    OOw[0]=OO
    TTw[0]=TT
    TOw[0]=TO

    LLw[0]=LL
    RRw[0]=RR
    LRw[0]=LR
    
    OLw[0]=OL
    ORw[0]=OR
    


    target[0]=cost2D.FindBin(c1,c2)    
    tt.Fill()

    vals= [Lep_pt1[0],Lep_eta1[0],Lep_phi1[0],Lep_pt2[0],Lep_eta2[0],Lep_phi2[0],target[0]]#,MEt_Et[0],MEt_Phi[0]]
#    for mi,v,ma in zip(xmin,vals,xmax):
#        if v < mi:print "Min",v
#        if v > ma:print "Max",v

#    b_h.Fill(array("d",vals),1)
#    pdb.set_trace()

b_h.Write()
rf_o.Write()
rf_o.Close()
cost.Fit("cts")
cost.Draw()
nom=fit_func.GetParameter(0)
fl_v=fit_func.GetParameter(1)
fr_v=fit_func.GetParameter(1)
f0_v=fit_func.GetParameter(1)


fl.SetParameter(0,nom)
fl.SetParameter(1,fl_v)
fr.SetParameter(0,nom)
fr.SetParameter(1,fr_v)
f0.SetParameter(0,nom)
f0.SetParameter(1,f0_v)

fl.Draw("same")
fr.Draw("same")
f0.Draw("same")

