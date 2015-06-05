import ROOT
from glob import glob
from array import array
import pdb

files=glob("./tests/test_plots/*.root")
files=[f for f in files if "true" not in f] ###bad naming

graph_points={}
for f in files:
    vals=[]
    rf=ROOT.TFile(f)
    c=rf.Get("cent_O")    
    u=rf.Get("uplimit_O")
    l=rf.Get("lowlimit_O")
    vals=[]
    x_bin=float(f.split("_")[-1].strip(".rot"))
    if x_bin==-1:x_bin=700
    lumi=[]
    for n in range(c.GetN()):        
        val=[]
        x=ROOT.Double()
        y=ROOT.Double()
        c.GetPoint(n,x,y)
        val.append(float(y))

        l.GetPoint(n,x,y)
        val.append(float(y))

        u.GetPoint(n,x,y)
        val.append(float(y)) 
        lumi.append(float(x))

        vals.append(val)
    print lumi
    for l,v in zip(lumi,vals):
        if graph_points.has_key(l):            
            graph_points[l][x_bin]=v
        else:
            graph_points[l]={x_bin:v}

for lumi in graph_points:
    bins=graph_points[lumi].keys()
    bins.sort()
    vals=[ graph_points[lumi][b] for b in bins]
    c=[i[0] for i in vals]    
    ul=[ i[2]-i[0] for i in vals]
    ll=[ i[0]-i[1] for i in vals]
    x_err=[0]+bins+[2*bins[-1]-bins[-2]]
 
    x= [(x+x1)/2. for x,x1 in zip(x_err[:-1],x_err[1:])]
    x_h= [(x1-x)/2. for x,x1 in zip(x_err[:-1],x_err[1:])]

    g=ROOT.TGraphAsymmErrors(len(c),array("f",bins),array("f",c),
                        array("f",x_h),array("f",x_h),
                        array("f",ll),array("f",ul))



    g.Draw("apl")
    pdb.set_trace()
