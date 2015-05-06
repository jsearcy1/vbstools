import ROOT
import pdb

rand=ROOT.TRandom()

in_rf=ROOT.TFile("temps_out.root")

BDT_h=in_rf.Get("BDT_h")
BDT_TT=in_rf.Get("BDT_TT")
BDT_TL=in_rf.Get("BDT_TL")
BDT_LL=in_rf.Get("BDT_LL")

BDT_h.Scale(3.13/BDT_h.Integral()) #1 fb worth of 13 TeV data




obj=ROOT.TObjArray()
obj.Add(BDT_TT)
obj.Add(BDT_TL)
obj.Add(BDT_LL)


n_trials=1000
LL_frac=ROOT.Double()
TL_frac=ROOT.Double()
TT_frac=ROOT.Double()
err=ROOT.Double()
res=ROOT.TH1F("f","f",1000,0,1)
for lumi in [1,10,100,300,3000]:
    TT_h=res.Clone()
    TT_h.SetName("TTf_"+str(lumi))
    TL_h=res.Clone()
    TL_h.SetName("TLf_"+str(lumi))
    LL_h=res.Clone()
    LL_h.SetName("LLf_"+str(lumi))

    for trial in range(n_trials):
        data=BDT_h.Clone()
        for i in range(1,data.GetNbinsX()+1):
            data.SetBinContent(i,rand.Poisson(BDT_h.GetBinContent(i)*lumi))
            data.SetBinError(i,data.GetBinContent(i)**.5)

        obj=ROOT.TObjArray()
        obj.Add(BDT_TT)
        obj.Add(BDT_TL)
        obj.Add(BDT_LL)

        tfit=ROOT.TFractionFitter(data,obj)
        tfit.Constrain(0,0,1)
        tfit.Constrain(1,0,1)
        tfit.Constrain(2,0,1)
        nfits=0
        while(tfit.Fit()!=0 and nfits <30):
            nfits+=1
        if nfits == 30:
            tfit.Delete()
            del tfit
            continue

        tfit.GetResult(0,TT_frac,err)        
        tfit.GetResult(1,TL_frac,err)
        tfit.GetResult(2,LL_frac,err)
        TT_h.Fill(TT_frac)
        TL_h.Fill(TL_frac)
        LL_h.Fill(LL_frac)

        if abs((TT_frac+TL_frac+LL_frac)-1) > .1:
            pdb.set_trace()
        tfit.Delete()
        del tfit
    exec "plot_"+str(lumi)+"=ROOT.TCanvas()"
    TT_h.SetLineColor(ROOT.kRed)
    TL_h.SetLineColor(ROOT.kBlue)
    LL_h.SetLineColor(ROOT.kGreen)
    TT_h.Draw()
    TL_h.Draw("same")
    LL_h.Draw("same")
    exec "plot_"+str(lumi)+".SaveAs('fplot"+str(lumi)+".root')"
