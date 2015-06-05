import ROOT
import sys
import pystlye
from array import array
in_files=sys.argv[1].split(",")

def GetTAG(rf,tag="O"):
    gu=rf.Get("uplimit_"+tag)
    gd=rf.Get("lowlimit_"+tag)
    gc=rf.Get("cent_"+tag)

    vals=[]
    for n in range(gu.GetN()):
        x=ROOT.Double()
        y=ROOT.Double()
        gc.GetPoint(n,x,y)
        cent=float(y)
        gu.GetPoint(n,x,y)
        u_e=y-cent
        gd.GetPoint(n,x,y)
        l_e=cent-y
        vals.append((x,cent,l_e,u_e))
    bin,c,ed,eu=zip(*vals)
    g=ROOT.TGraphAsymmErrors(len(bin),array("f",bin),array("f",c),array("f",[0]*len(bin)),array("f",[0]*len(bin)),array("f",ed),array("f",eu) )
    return g


for f in in_files:
    rf=ROOT.TFile(f)
    for i,tag in enumerate(["OO","OL","OR","LL","LR","RR"]):
        exec "g"+tag+"=GetTAG(rf,'"+tag+ "')"
        exec "g"+tag+".SetLineColor(pytstyle.colors[i])"
        exec "g"+tag+".SetFillColor(pytstyle.colors[i])"
        exec "g"+tag+".SetFillSytle(3003)"

c1=ROOT.TCavnas()
p1=ROOT.TPad("1","1",0,0,1,0.5)
p2=ROOT.TPad("2","2",0,0.5,1,1)

p1.cd()


