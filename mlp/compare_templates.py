import ROOT
import sys
import pdb

def comp_plot(h1,h2,name1="",name2=""):
    c1=ROOT.TCanvas()

    h1.Scale(1./h1.GetSum())
    h2.Scale(1./h2.GetSum())
    maximum=max([h1.GetMaximum(),h2.GetMaximum()])*1.2
    h1.SetLineColor(ROOT.kRed)
    h1.SetMaximum(maximum)
    leg=ROOT.TLegend(0.6,0.6,0.8,0.8)    
    leg.SetFillColor(ROOT.kWhite)
    leg.SetLineColor(ROOT.kWhite)
    leg.AddEntry(h1,name1)
    leg.AddEntry(h2,name2)
    h1.Draw()
    h2.Draw("same")
    leg.Draw("same")
    return c1,leg,h1,h2
    


if __name__=="__main__":
    rf1=ROOT.TFile(sys.argv[1])    
    rf2=ROOT.TFile(sys.argv[2])
    canvas=[]
    for name in ["O","L","R"]:
        h1=rf1.Get(name)
        h2=rf2.Get(name)
        canvas.append(comp_plot(h1,h2,sys.argv[1],sys.argv[2]))
