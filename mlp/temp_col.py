import ROOT
import sys
import pdb

rf=ROOT.TFile(sys.argv[1])
fit_func=ROOT.TF1("cts","(3/8*(1-x)^2*[0] +3/8*(1+x)^2*[1]+3/4*(1-x^2)*[2\
])",-.8,1)

fit_l=ROOT.TF1("l","(3/8*(1-x)^2*[0])",-.8,1)

fit_r=ROOT.TF1("r","(3/8*(1+x)^2*[0])",-.8,1)

fit_o=ROOT.TF1("o","(3/4*(1-x^2)*[0])",-.8,1)



ctsb=rf.Get("cts_b")
ctsa=rf.Get("cts_a")
L=rf.Get("L")
R=rf.Get("R")
O=rf.Get("O")
data=rf.Get("nor")
c0=ROOT.TCanvas()
All=L.Clone()
All.Add(R)
All.Add(O)
All.Draw()
data.Draw("same")
pdb.set_trace()

###############
c1=ROOT.TCanvas()
start_bin=ctsa.FindBin(-.6)
end_bin=ctsa.GetNbinsX()
start_range=ctsa.GetBinLowEdge(start_bin)
end_range=ctsa.GetBinLowEdge(end_bin+1)

ctsb.GetXaxis().SetRange(start_bin,ctsb.GetNbinsX()) #avoids the clipped region
ctsb.Scale(1./ctsb.Integral()) #dosen't scale far enough fix later
ctsb.Fit("cts")

ctsb.Scale(fit_func.Integral(start_range,1)/fit_func.Integral(-1,1))
ctsb.Fit("cts")

###############
c4=ROOT.TCanvas()
ctsa.GetXaxis().SetRange(start_bin,ctsa.GetNbinsX()) #avoids the clipped region
ctsa.Scale(1./ctsa.Integral()) #dosen't scale far enough fix later
ctsa.Fit("cts")

ctsa.Scale(fit_func.Integral(start_range,1)/fit_func.Integral(-1,1))
ctsa.Fit("cts")

fl=fit_func.GetParameter(0)
fr=fit_func.GetParameter(1)
fo=fit_func.GetParameter(2)


### fix for clipped bit
fit_l.SetParameter(0,fl)
fit_r.SetParameter(0,fr)
fit_o.SetParameter(0,fo)
###########################


fl=(fl)/ctsa.GetBinWidth(1)
fr=(fr)/ctsa.GetBinWidth(1)
fo=(fo)/ctsa.GetBinWidth(1)



ceff=ctsa.Integral(0,start_bin)/(fit_func.Integral(-1,start_range)/ctsa.GetBinWidth(1)) #this is the efficiency of cuts in the non-fitte costheat*
norm=fit_func.Integral(-1,start_range)*ceff+fit_func.Integral(start_range,1)

fl_norm=(fit_l.Integral(-1,start_range)*ceff+fit_l.Integral(start_range,1))/norm
fr_norm=(fit_r.Integral(-1,start_range)*ceff+fit_r.Integral(start_range,1))/norm
fo_norm=(fit_o.Integral(-1,start_range)*ceff+fit_o.Integral(start_range,1))/norm

#pdb.set_trace()

ctsa.Draw()




c2=ROOT.TCanvas()
L.Scale(data.Integral(0,10000)*fl_norm/L.Integral())
R.Scale(data.Integral(0,10000)*fr_norm/R.Integral())
O.Scale(data.Integral(0,10000)*fo_norm/O.Integral())

hall=L.Clone()
hall.Add(R)
hall.Add(O)
hall.SetLineColor(ROOT.kRed)
hall.Draw()
data.Draw("same")

temps=ROOT.TObjArray()

L.Scale(10000)
R.Scale(10000)
O.Scale(10000)

temps.Add(L)
temps.Add(R)
temps.Add(O)

fit=ROOT.TFractionFitter(data,temps,"")
fit.Constrain(0,0,1)
fit.Constrain(1,0,1)
fit.Constrain(2,0,1)
fit.Fit()
fl_2=ROOT.Double()
fr_2=ROOT.Double()
fo_2=ROOT.Double()
err=ROOT.Double()

fit.GetResult(0,fl_2,err)
fit.GetResult(1,fr_2,err)
fit.GetResult(2,fo_2,err)


c3=ROOT.TCanvas()
fit.GetPlot().Draw()
data.Draw("same")


