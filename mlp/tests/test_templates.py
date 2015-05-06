import ROOT
from numpy.random import poisson
import pdb

colors=[ROOT.kGreen,ROOT.kRed+1,ROOT.kRed,ROOT.kRed-1,ROOT.kBlue,ROOT.kBlue-1]


rf=ROOT.TFile("ct_templates.root")
hists=[]
for hname in ["OOw","LRw","RRw","LLw","OLw","ORw"]:
    hists.append(rf.Get(hname))

h_L=rf.Get("L")
h_R=rf.Get("R")
h_O=rf.Get("O")
h_norm1d=rf.Get("nor")
norm=rf.Get("norm")
#h_L.Scale(100000000.)
#h_R.Scale(100000000.)
#h_O.Scale(100000000.)

h_L.Sumw2()
h_R.Sumw2()
h_O.Sumw2()

mc=ROOT.TObjArray(len(hists))
for h in hists:
    mc.Add(h)
fit=ROOT.TFractionFitter(norm,mc)
for i in range(len(hists)):    
    fit.Constrain(i,0,1.0)
fit.Fit()


def draw_test(hists,data,fit1D):
    stack1d=ROOT.THStack()
    x=fit1D.GetPlot()
    for i,h in enumerate(hists):
        res=ROOT.Double()
        err=ROOT.Double()

        fit1D.GetResult(i,res,err)
        h.Scale(res*test.Integral()*1./h.Integral())
        h.SetLineColor(colors[i])
        h.SetFillColor(colors[i])
        stack1d.Add(h)
    stack1d.Draw("hist")
    data.Draw("same E")
    x.Draw("same")
    pdb.set_trace()


def unfold(hist):
    x=hist.GetNbinsX()
    y=hist.GetNbinsY()
    n_hist=ROOT.TH1F("oneD"+hist.GetName(),"oneD"+hist.GetName(),x*y,0,x*y)
    b_num=1
    for bin_x in range(1,x+1):
        for bin_y in range(1,y+1):
            con=hist.GetBinContent(bin_x,bin_y)
            err=hist.GetBinError(bin_x,bin_y)
            n_hist.SetBinContent(b_num,con)            
            n_hist.SetBinError(b_num,err)
            b_num+=1
    return n_hist
un_norm=unfold(norm)
fit_r=unfold(fit.GetPlot())
c1=ROOT.TCanvas()
fit_r.Draw("hist")
 
un_hists=[]
for h in hists:
    un_hists.append(unfold(h))


stack=ROOT.THStack()
for i,h in enumerate(un_hists):
    res=ROOT.Double()
    err=ROOT.Double()
    fit.GetResult(i,res,err)
    h.Scale(res*un_norm.Integral()*1./h.Integral()   )
    h.SetLineColor(colors[i])
    h.SetFillColor(colors[i])
    h.Draw("same")
    stack.Add(h)
stack.Draw("hist")
un_norm.Draw("same")

fit.Delete()
del fit

c2=ROOT.TCanvas()



mc1d=ROOT.TObjArray(len(hists))
for h in [h_O,h_L,h_R]:
    mc1d.Add(h)
h_O.DrawNormalized()
h_L.DrawNormalized("same")
h_R.DrawNormalized("same")
pdb.set_trace()
events=[40.,400.,1200.,12000.]
vals=[]
errs=[]
hh=[]
for evt in events:
    h_Of=ROOT.TH1F("valo"+str(evt),"valo"+str(evt),100,0,1)
    h_Lf=ROOT.TH1F("vall"+str(evt),"vall"+str(evt),100,0,1)
    h_Rf=ROOT.TH1F("valr"+str(evt),"valr"+str(evt),100,0,1)
    h_Of.SetLineColor(ROOT.kGreen)
    h_Lf.SetLineColor(ROOT.kRed)
    hh.append([h_Of,h_Lf,h_Rf])
    for i in range(1000):
        mc1d=ROOT.TObjArray(len(hists))
        for h in [h_O,h_L,h_R]:
            mc1d.Add(h.Clone())
        print "start test 2"
        test=h_norm1d.Clone()
        test.Scale(2*evt/test.Integral()) # 2* is because you have 2 Ws
        print test.Integral()
        for i in range(test.GetNbinsX()):
            con=test.GetBinContent(i)
            n_con=poisson(con)
            test.SetBinContent(i,n_con)
            test.SetBinError(i,n_con**.5)
        print test.Integral()
        fit1D=ROOT.TFractionFitter(test,mc1d,"v")
        fit1D.Constrain(0,0,1)
        fit1D.Constrain(1,0,1)
        fit1D.Constrain(2,0,1)
        nfits=0
        fit_max=20
        fit1D.Fit()
        while(fit1D.Fit()!=0 and nfits < fit_max):
            nfits+=1
        print nfits
        if nfits==fit_max:
            fit1D.Delete()
            del fit1D
            continue
        res=ROOT.Double()
        err=ROOT.Double()
        fit1D.GetResult(0,res,err)
        v0=float(res);e0=float(err)
        fit1D.GetResult(1,res,err)
        v1=float(res);e1=float(err)
        fit1D.GetResult(2,res,err)
        v2=float(res);e2=float(err)
        vals.append([v0,v1,v2])
        errs.append([e0,e1,e2])
        h_Of.Fill(v0)
        h_Lf.Fill(v1)
        h_Rf.Fill(v2)
        #draw_test([h_O.Clone(),h_L.Clone(),h_R.Clone()],test,fit1D)
        fit1D.Delete()
        mc1d.Delete()
        del mc1d
        del fit1D
    h_Of.Draw()
    h_Lf.Draw("same")
    h_Rf.Draw("same")
    raw_input()




