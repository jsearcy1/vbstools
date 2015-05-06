from pol_tools import  *
import ROOT

rf=ROOT.TFile("~/Desktop/lhe_converter/unweighted_events.lhe.1.root")
tree=rf.Get("truth")
cost=ROOT.TH1F("cts","cts",20,-1,1)
fit_func=ROOT.TF1("cts","[0]*(3/8*(1-x)^2*[1] +3/8*(1+x)^2*[2]+3/4*(1-x^2)*[3])",-.8,1)
fit_func2=ROOT.TF2("cts2","(3/8*(1-x)^2*[1] +3/8*(1+x)^2*[2]+3/4*(1-x^2)*[3])*(3/8*(1-y)^2*[1] +3/8*(1+y)^2*[2]+3/4*(1-y^2)*[3])",-.8,1)


M_ww_bins=10
M_ww_max=1000

for bom in range(M_ww_bins):
    Mww_arr.append(ROOT.TH2F("ct2"+str(bin),"ct2"+str(bin),10,-.8,1,10,-.8,1))
    
for evt in range(tree.GetEntries()):
    tree.GetEntry(evt)
    W1,W2=Get4Vects(tree)
    l1,n1=W1
    l2,n2=W2
 
    Wv1=l1+n1
    Wv2=l2+n2
    print Wv1.Pt(),l1.Pt()
    c1=GetCosThetaS(W2)
    c2=GetCosThetaS(W1)
    Mww=(Wv1+Wv2).M()
    Mww_arr           ##this is an array should be filled by casting and int, doing fits etc, but I'm try what I already have first    
    
   

