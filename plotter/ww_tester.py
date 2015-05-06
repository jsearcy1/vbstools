from pol_tools import  *
import ROOT

rf=ROOT.TFile("~/Desktop/lhe_converter/unweighted_events.lhe.1.root")
tree=rf.Get("truth")
cost=ROOT.TH1F("cts","cts",20,-1,1)
fit_func=ROOT.TF1("cts","[0]*(3/8*(1-x)^2*[1] +3/8*(1+x)^2*[2]+3/4*(1-x^2)*[3])",-.8,1)

for evt in range(tree.GetEntries()):
    tree.GetEntry(evt)
    W1,W2=Get4Vects(tree)

#    Boost_evt_rest(W1+W2+[j1]+[j2])

    l1,n1=W1
    l2,n2=W2

    Wv1=l1+n1
    Wv2=l2+n2
    print Wv1.Pt(),l1.Pt()

    c1=GetCosThetaS(W2)
    c2=GetCosThetaS(W1)
    cost.Fill(c1)
    cost.Fill(c2)
#    cost2D.Fill(c1,c2) # Should we sort c1 c2?
    

