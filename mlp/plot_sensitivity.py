import ROOT
import os
import sys
import cPickle
import pdb
import pystyle
from array import array

labels={"nOO":"TT+LT",
        "OOw":"LL",
        "LLw":"Left-Left",
        "RRw":"Right-Right",
        "LRw":"Left-Right",
        "OLw":"Longitudinal-Left",
        "ORw":"Longitudinal-Right",
        "OOw":"Longitudinal-Longitudinal",
        "OT":"Longitudinal-Transverse",
        "TT":"Transverse-Transverse"
}





def GetPlot(in_vals):
    g1=ROOT.TGraphAsymmErrors(len(in_vals))
    g2=ROOT.TGraphAsymmErrors(len(in_vals))
    for i,v in enumerate(in_vals):
        g1.SetPoint(i,v["lumi"],v["mean"])
        g2.SetPoint(i,v["lumi"],v["mean"])
        

        g1.SetPointEYlow(i,v["mean"]-v["68"][0])
        g1.SetPointEYhigh(i,v["68"][1]-v["mean"])
        g2.SetPointEYlow(i,v["mean"]-v["95"][0])
        g2.SetPointEYhigh(i,v["95"][1]-v["mean"])
        g1.SetFillColor(ROOT.kYellow)
        g2.SetFillColor(ROOT.kGreen)    
    return g1,g2

in_files=sys.argv[1].split(",")
out_file=sys.argv[2]
gs=[]
ls=[]
ts=[]
start=True
w_step=1./len(in_files)
w_pads=[]
for w,f in enumerate(in_files):
    

    out_dict=cPickle.load(open("tests/test_output/"+f))

    graphs=len(out_dict)
    if start:
        c1=ROOT.TCanvas("C1","C1",400*len(in_files),300*graphs)
        start=False
    c1.cd()
    w_pad=ROOT.TPad(f,f,w*w_step,0,(w+1)*w_step,1)
    w_pads.append(w_pad)
    w_pad.Draw()
    w_pad.cd()
    if "pol_ratio" in f:
        title="Fit Precision with RpT"
    else:
        title="Fit Precision with NN"

    t=ROOT.TText(.1,.97,title)
    
    t.SetTextSize(.07)
    t.Draw()
    ts.append(t)


#    print graphs
    pads=[]

    for i in range(graphs):
        step=.95/graphs
        #print 0,i*step,1,1,(i+1.)*step
        print str(i)+f
        pads.append(ROOT.TPad(str(i)+f,str(i)+f,0,i*step,1,(i+1.)*step ))



    for p in pads:
        p.SetTopMargin(0.02)
    for p in pads:
        p.Draw()

    for k,p in zip(out_dict,pads):
        p.cd()
        g1,g2=GetPlot(out_dict[k])
#        pdb.set_trace()

        x=ROOT.Double()
        y=ROOT.Double()
        g2.GetPoint(g2.GetN()-1,x,y)

        gs.append([g1,g2,p])
        g1.SetMinimum(-0.01)
        g2.SetMinimum(-0.01)
        g1.SetMaximum(1.01)
        g2.SetMaximum(1.01)        
#        g2.GetXaxis().SetTitle("fb^{-1}")
#        g2.GetYaxis().SetTitle("Fraction")

        g2.GetXaxis().SetLabelSize(0.07)
        g2.GetYaxis().SetLabelSize(0.09)
        g2.GetXaxis().SetLimits(10,3000)

        g2.Draw("ape3")
        g1.Draw("pe3")
        print y
        tl=ROOT.TLine(10,y,3000,y)
        tl.SetLineWidth(2)
        tl.Draw()
        ls.append(tl)
      
        p.RedrawAxis()
        l1=ROOT.TLatex(1000,.7,labels[k])
        l2=ROOT.TLatex(3050,.0,"fb^{-1}")
        
        l1.SetTextSize(.02*graphs)
        l2.SetTextSize(.02*graphs)
        l1.Draw()
        l2.Draw()
        ls.append(l1)
        ls.append(l2)
c1.SaveAs(out_file+".root")    
c1.SaveAs(out_file+".png")    
c1.SaveAs(out_file+".pdf")    
