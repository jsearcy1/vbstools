import ROOT
import os
import gc
from optparse import OptionParser
from numpy.random import poisson
from array import array
import pdb
import resource
import cPickle
ROOT.gErrorIgnoreLevel=ROOT.kFatal
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING) 
ROOT.SetMemoryPolicy( ROOT.kMemoryStrict )
ROOT.RooTrace.active(1)
ROOT.RooRealVar.__init__._creates=1
ROOT.RooArgList.__init__._creates=1
ROOT.RooArgSet.__init__._creates=1
ROOT.RooDataHist.__init__._creates=1
ROOT.RooHistPdf.__init__._creates=1

def FractionFitter(templates,data):
    

    x= ROOT.RooRealVar("x","x",data.GetXaxis().GetBinLowEdge(1),data.GetXaxis().GetBinLowEdge(data.GetNbinsX()+1)) 
    y= ROOT.RooRealVar("y","y",data.GetYaxis().GetBinLowEdge(1),data.GetYaxis().GetBinLowEdge(data.GetNbinsY()+1)) 

    if type(data)==ROOT.TH2F:
        oneD=False
    else:
        oneD=True
    

    fractions=[]
    for i in range(len(templates)):
        fractions.append(ROOT.RooRealVar("f"+str(i),"f"+str(i),0,data.Integral()))
        
        

    h_sets=[]
    hh=[]
    rhpdf=[]
    if oneD:
        ral=ROOT.RooArgList(x)
        ras=ROOT.RooArgSet(x)
    else: 
        ral=ROOT.RooArgList(x,y)
        ras=ROOT.RooArgSet(x,y)

    data_rds=ROOT.RooDataHist(data.GetName()+"ds",data.GetName()+"ds",ral,data)
    for h in templates:
        rds=ROOT.RooDataHist(h.GetName()+"ds",h.GetName()+"ds",ral,h)
        rhpdf.append(ROOT.RooHistPdf(h.GetName()+"pdf",h.GetName()+"pdf",ras,rds))
        hh.append(rds)
    pdf_l=ROOT.RooArgList(*rhpdf)
    pdf=ROOT.RooAddPdf("fitter","fiter",pdf_l,ROOT.RooArgList(*fractions))
    pdf.fitTo(data_rds,ROOT.RooFit.PrintLevel(-100000),ROOT.RooFit.SumW2Error(False))

    colors=[ROOT.kGreen,ROOT.kRed+1,ROOT.kRed,ROOT.kRed-1,ROOT.kBlue,ROOT.kBlue-1]
    draw=False

    
    if draw:
        stack=ROOT.THStack("stack","stack")
        for i,h,frac in zip(range(len(templates)),templates,[v.getVal() for v in fractions]):
            h.Scale(frac/h.Integral())
            if type(h)==ROOT.TH2F:
                h2=unfold(h)
            else:
                h2=h
            h2.SetFillColor(colors[i])
            h2.SetLineColor(colors[i])
            stack.Add(h2)
            hh.append(h2)
        if type(data)==ROOT.TH2F:
                data2=unfold(data)
        else:
            data2=data
        stack.Draw("hist")
        data2.Draw("same E")
    if draw:pdb.set_trace()
        
    values=[v.getVal()/data.Integral() for v in fractions]

    return values
     

def Limit(h):
    mean=h.GetMean()
    ulimit68=None
    ulimit95=None
    llimit68=None
    llimit95=None
    trials=float(h.GetSum())
    for i in range(h.GetNbinsX()):
        
        utrials=h.Integral(i,10000)/trials
        ltrials=h.Integral(0,i)/trials
        #print i,utrials,ltrials, ulimit68,ulimit95,llimit68, llimit95
        if ulimit68==None and utrials < 0.16:
            ulimit68=h.GetBinLowEdge(i)
        if ulimit95==None and utrials < 0.025:
            ulimit95=h.GetBinLowEdge(i)
        if llimit68==None and ltrials > 0.16:
            llimit68=h.GetBinLowEdge(i)
        if llimit95==None and ltrials > 0.025:
            llimit95=h.GetBinLowEdge(i)
    if ulimit68==None:ulimit68=1
    if ulimit95==None:ulimit95=1
    if llimit68==None:llimit68=0.0
    if llimit95==None:llimit95=0.0

    return [llimit95,ulimit95,llimit68,ulimit68]

def unfold(h):
    nbins_x=h.GetNbinsX()
    nbins_y=h.GetNbinsY()

    uh=ROOT.TH1F(h.GetName()+"_unfold",h.GetName()+"_unfold",nbins_x*nbins_y,0,nbins_x*nbins_y)
    uh.SetDirectory(0)
    bn=0
    for x in range(1,nbins_x+1):
        for y in range(1,nbins_y+1):
            bn+=1
            uh.SetBinContent(bn,h.GetBinContent(x,y))
            uh.SetBinError(bn,h.GetBinError(x,y))
            
    return uh

 
def fit(templates,data):
    values=FractionFitter(templates,test)

    return values



def draw_test(hists,data,fit1D,lumi=1):
#    c1=ROOT.TCanvas()
    colors=[ROOT.kGreen,ROOT.kRed+1,ROOT.kRed,ROOT.kRed-1,ROOT.kBlue,ROOT.kBlue-1]
    stack1d=ROOT.THStack()
    x=fit1D.GetPlot()
    hh=[]


    for i,h in enumerate(hists):
        res=ROOT.Double()
        err=ROOT.Double()
        if type(h)==ROOT.TH2F:
            draw_h=unfold(h)
        else:
            draw_h=h
        hh.append(draw_h)
        if x:
            fit1D.GetResult(i,res,err)
            draw_h.Scale(res*data.Integral()*1./draw_h.Integral())
        else:
            h.Scale(lumi/100000.)
        draw_h.SetLineColor(colors[i])
        draw_h.SetFillColor(colors[i]) 
        stack1d.Add(draw_h)
    stack1d.Draw("hist")
    
    if type(data)==ROOT.TH2F:
        data=unfold(data)
        if x: x=unfold(x)
    data.Draw("same E")
    if x: x.Draw("same")

    pdb.set_trace()



def Get_templates(rf,fit_type):
    h_L=rf.Get("L")
    h_R=rf.Get("R")
    h_O=rf.Get("O")

    h_LL=rf.Get("LLw")
    h_RR=rf.Get("RRw")
    h_OO=rf.Get("OOw")
    h_OL=rf.Get("OLw")
    h_OR=rf.Get("ORw")
    h_LR=rf.Get("LRw")

    h_TT=h_LL.Clone()
    h_TT.SetName("TT");h_TT.SetTitle("TT")
    h_TT.Add(h_RR)
    h_TT.Add(h_LR)

    h_OT=h_OL.Clone()
    h_OT.SetName("OT");h_OT.SetTitle("OT")
    h_OT.Add(h_OR)
    

    h_All_t=h_LL.Clone()
    h_All_t.SetName("nOO");h_All_t.SetTitle("nOO")
    h_All_t.Add(h_RR)
    h_All_t.Add(h_OL)
    h_All_t.Add(h_OR)
    h_All_t.Add(h_LR)

    
    h_T=h_L.Clone()
    start_range=0
    end_range=h_L.GetNbinsX()

    h_norm1d=rf.Get("nor")
    norm=rf.Get("norm")

    h_L.Sumw2()
    h_R.Sumw2()
    h_O.Sumw2()


    h_tmp=h_R.Clone()
    h_tmp.Scale(1./h_tmp.GetSum())
    h_T.Scale(1./h_T.GetSum())
    h_T.Add(h_tmp,1.18)
    h_T.Scale(10000.)
    
    
    if fit_type==0:
        return [h_LL,h_LR,h_RR,h_OL,h_OR,h_OO],norm
    elif fit_type==1:
        return [h_TT,h_OT,h_OO],norm
    elif fit_type==2:
        return [h_All_t,h_OO],norm
    else:
        print "Invalid fit type"
        return -1
    

def GetNewData(data,lumi):
    new_data=data.Clone()
    new_data.Scale(lumi)
    if type(new_data)==ROOT.TH2F:
        for x in range(new_data.GetNbinsX()):
            for y in range(new_data.GetNbinsY()):
                con=new_data.GetBinContent(x,y)
                n_con=poisson(con)
                new_data.SetBinContent(x,y,n_con)
                new_data.SetBinError(x,y,n_con**.5)
    else:
        for i in range(new_data.GetNbinsX()):
            con=new_data.GetBinContent(i)
            n_con=poisson(con)
            new_data.SetBinContent(i,n_con)
            new_data.SetBinError(i,n_con**.5)
    return new_data


def test_fits(lumi,b_templates,data,n_trials=1,oneD=True):
    p_hs=[]
    o=None
    for p,h in enumerate(b_templates):
        p_hs.append(ROOT.TH1F("val_"+h.GetName()+"_"+str(int(lumi))+"fb","val_"+h.GetName()+"_"+str(int(lumi))+"fb",2000,0,1))            
    for i in range(n_trials):
        templates=[h.Clone() for h in b_templates]
        new_data=GetNewData(data,lumi)
        values=FractionFitter(templates,new_data)
        for param in range(len(templates)):
            p_hs[param].Fill(values[param])
    gc.collect()
    return p_hs


if __name__ == "__main__":   
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="in_file",
                      help="input template file", default="../ct_templates.root")
    parser.add_option("-l", "--lumi", dest="lumi",
                      help="Luminosity to normalize data too", default="1000")
    parser.add_option("-T", dest="fit_type",type="int",
                      help="Type of fit", default=0)

    (options, args) = parser.parse_args()

    lumi=[float(i) for i in options.lumi.split(",")]
    rf=ROOT.TFile(options.in_file)
    templates,data= Get_templates(rf,options.fit_type)
    Names=[h.GetName() for h in templates]

    values={}
    for n in Names:
        values[n]=[]
    
    all_hists=[]
    for l in lumi:
        hists=test_fits(l,templates,data,n_trials=10000)
        all_hists+=hists
        for n,h in zip(Names,hists):
            low95,high95,low68,high68=Limit(h)
            values[n].append({"lumi":l,"mean":h.GetMean(),"68":[low68,high68],"95":[low95,high95]})
    f_base=os.path.split(options.in_file)[1]
    out_file="".join( f_base.split(",")[:-1])
    if out_file=="":
        out_file=f_base
    out_file+="_"+str(options.fit_type)
    
 #   rf.Close()
    out_rf=ROOT.TFile("test_output/"+out_file+".root","Recreate")
    out_rf.cd()
    for h in all_hists:
        h.SetDirectory(out_rf)
        h.Write()
    out_rf.Close()
    rf.Close()
    out_pickle= cPickle.dump(values,open("test_output/"+out_file+".pk","w"))        
    
