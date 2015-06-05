import ROOT
import gc
from optparse import OptionParser
from numpy.random import poisson
from array import array
import pdb
import resource
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
    x= ROOT.RooRealVar("x","x",-1,1) 
    y= ROOT.RooRealVar("y","y",-1,1) 

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

    if oneD and draw:
        data_rds.plotOn(f)
        pdf.plotOn(f)
        f.Draw()
    elif draw:
        stack=ROOT.THStack("stack","stack")
        for i,h,frac in zip(range(len(templates)),templates,[v.getVal() for v in fractions]):
            h.Scale(frac/h.Integral())
            h2=unfold(h)
            h2.SetFillColor(colors[i])
            h2.SetLineColor(colors[i])
            stack.Add(h2)
            hh.append(h2)
        data2=unfold(data)
        stack.Draw("hist")
        data2.Draw("same E")
 #       pdb.set_trace()
#    raw_input()
        
    values=[v.getVal()/data.Integral() for v in fractions]
#    pdb.set_trace()
#    del ras

   

#    for h in list(locals().values()):
#        try:ROOT.SetOwnership(h,False)
#        except:pass
        #if hasattr(h, '__iter__'):
        #    try: [n.Delete() for n in h]
        #    except:pass
        #try: h.Delete()
        #except:pass
        #del h
#    pdb.set_trace()

#    ras.cleanup()
#    [fr.Delete() for fr in fractions]
#    x.Delete()
#    y.Delete()
#    pdb.set_trace()
#    ROOT.RooTrace.dump()

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
#    pdb.set_trace()
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

 
def test_fit(templates,data,lumi,start=None,stop=None):
    mc1d=ROOT.TObjArray(len(templates))
    for h in templates:
        if start and stop:
            h.GetXaxis().SetRange(start,stop)
        mc1d.Add(h)
#    print "start test 2"
    test=data.Clone()
    test.Scale(lumi) # This should already be normalized to fb
#    print test.Integral()
#    pdb.set_trace()

    if type(test)==ROOT.TH2F:
        for x in range(test.GetNbinsX()):
            for y in range(test.GetNbinsY()):
                con=test.GetBinContent(x,y)
                n_con=poisson(con)
                test.SetBinContent(x,y,n_con)
                test.SetBinError(x,y,n_con**.5)
    else:

        for i in range(test.GetNbinsX()):
            con=test.GetBinContent(i)
            n_con=poisson(con)
            test.SetBinContent(i,n_con)
            test.SetBinError(i,n_con**.5)
#    print test.Integral()
    if start and stop:
        test.GetXaxis().SetRange(start,stop)
    values=FractionFitter(templates,test)
#    print ROOT.RooTrace.dump()
#    pdb.set_trace()

#    fit1D=ROOT.TFractionFitter(test,mc1d,"")
#    for param in range(len(templates)):
#        fit1D.Constrain(param,0,1)
#    fit1D.ErrorAnalysis(.001)
#    nfits=0
#    fit_max=20
#    while(fit1D.Fit()!=0 and nfits < fit_max):
#        nfits+=1
#        print nfits
#    if nfits==fit_max:
#        print "Fit did not converge!!"
#        return fit1D,test,0
    
#    fit_test(templates[0],templates[1],templates[2],test)
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

#    pdb.set_trace()


def test_fits(events,rf,n_trials=1,oneD=True):
    h_L=rf.Get("L")
    h_R=rf.Get("R")
    h_O=rf.Get("O")

    h_LL=rf.Get("LLw")
    h_RR=rf.Get("RRw")
    h_OO=rf.Get("OOw")
    h_OL=rf.Get("OLw")
    h_OR=rf.Get("ORw")
    h_LR=rf.Get("LRw")

    

    for h in [h_L,h_R,h_O,h_LL,h_RR,h_OO,h_OL,h_OR,h_LR]:
        #h.Scale(h.GetEntries()/h.Integral()) #saves the reall stat errore
        h.Scale(100000.)
    h_T=h_L.Clone()
    start_range=0
    end_range=h_L.GetNbinsX()
    found_data=False
    for i in range(h_L.GetNbinsX()):
        if (h_L.GetBinContent(i)==0 or h_R.GetBinContent(i)==0 
            or h_O.GetBinContent(i)==0):
            if not found_data:
                start_range=i+1
            else:
                end_range=i-1
                break
        else:
            found_data=True
    for h in [h_R,h_O,h_L,h_T]:
        h.GetXaxis().SetRange(start_range,end_range)
    

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
    

    vals=[]
    errs=[]
    hh=[]
    
    if oneD:
        b_templates=[h_O,h_L,h_R]
    else:
        b_templates=[h_OO,h_LL,h_RR,
                 h_OR,h_OL,h_LR]

#    FractionFitter(b_templates,h_norm1d)
#    pdb.set_trace()

    results=[[] for i in range(len(b_templates))]
    old_d={}
    for evt in events: 

        p_hs=[]
        o=None
        for p in range(len(b_templates)):
            p_hs.append(ROOT.TH1F("val"+str(p)+"_"+str(evt),"valo"+str(evt),200,0,1))            
        for i in range(n_trials):
            templates=[h.Clone() for h in b_templates]
#            fit1D,test=test_fit(templates,h_norm1d,evt,start_range,end_range)

#            templates=[h_OO.Clone(),h_LL.Clone(),h_RR.Clone(),
#                       h_OR.Clone(),h_OL.Clone(),h_LR.Clone()]
            if oneD:
                values=test_fit(templates,h_norm1d,evt,start_range,end_range)
            else:
                values=test_fit(templates,norm,evt,start_range,end_range)
 #           pdb.set_trace()
#            fit1D,test=test_fit(templates,h_norm1d,evt,start_range,end_range)
#            if err== 0 :
#                draw_test(templates,test,fit1D,evt)                                
#                del fit1D
#                continue
##            draw_test(templates,test,fit1D)                                
#            res=ROOT.Double()
#            err=ROOT.Double()

#            t_val=[]
            for param in range(len(templates)):
#                fit1D.GetResult(param,res,err)
#                t_val.append(float(res))
                p_hs[param].Fill(values[param])
            vals.append(values)
#            errs.append([e0,e1,e2])
#            h_Of.Fill(v0)
#            h_Lf.Fill(v1)
#            h_Rf.Fill(v2)
#            pdb.set_trace()
#            if i<5 and doTest:
#                c2=ROOT.TCanvas()

#            pdb.set_trace()
#            fit1D.Delete()
#            del fit1D

            print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            gc.collect()
            #pdb.set_trace()
            # ts=[type(g) for g in gc.get_objects()]
            # z={}
            # for t in ts:
            #     if z.has_key(t):
            #         z[t]+=1
            #     else:
            #         z[t]=1
            # for name in z:
            #    try: 
            #        if old_d[name]!=z[name]:
            #            print name,z[name]
            #    except(KeyError):
            #        print name,z[name]
            # old_d=z
            # pdb.set_trace()            
            

#            c1=ROOT.TCanvas()

        #h_Of.DrawNormalized()
        #h_Lf.DrawNormalized("same")
       # h_Rf.DrawNormalized("same")
        limits=[ [h]+Limit(h) for h in p_hs]
        p_hs[0].Draw()
        [h.Draw("same") for h in p_hs[1:]]
#        pdb.set_trace()
        #ulo=Limit(h_Of)
        #ull=Limit(h_Lf)
        #ulr=Limit(h_Rf)

        
        print limits
        pdb.set_trace()
        for n,vals in enumerate(limits):      
#            pdb.set_trace()
            h,lo,up,lo68,up68=vals
            results[n].append([h.GetMean(),lo68,up68])
            h.Reset()
    return results



if __name__ == "__main__":   
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="in_file",
                      help="input template file", default="../ct_templates.root")
    parser.add_option("-o", "--out_file", dest="out_file",
                      help="input template file", default="./outplots.root")
    parser.add_option("-l", "--lumi", dest="lumi",
                      help="Luminosity to normalize data too", default="100")
    parser.add_option("-D", "", dest="Dem",type="int",
                      help="1 or 2 number of dimentions", default=1)

    (options, args) = parser.parse_args()

    lumi=[float(i) for i in options.lumi.split(",")]
    if options.Dem==1:
        oneD=True
    elif options.Dem==2:
        oneD=False
    else:
        print "Invalid Dimention assume 1D"
        oneD=True
        

    rf=ROOT.TFile(options.in_file)
    res_cont=test_fits(lumi,rf,5000,oneD)
    gp_cont=[]
    
    colors=[ROOT.kRed,ROOT.kBlue,ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kViolet]
#    names=["0","1","2","3","4","5","6"]
    if oneD:
        names=["O","L","R"]
    else:
        names=["OO","LL","RR","OR","OL","LR"]



    leg=ROOT.TLegend(0.6,0.6,0.8,0.8)

    for n,res in enumerate(res_cont):    
        res_c=[i[0] for i in res]
        res_l=[i[1] for i in res]
        res_u=[i[2] for i in res]

#        graph=ROOT.TGraphErrors(len(res_c),array("f",[l+max(lumi)*.01*n for l in lumi]),array("f",res_c),array("f",[0]*len(res_c)),array("f",res_e))
        g1=ROOT.TGraph(len(res_l),array("f",[l+max(lumi)*.001*n for l in lumi]),array("f",res_c))
        gl=ROOT.TGraph(len(res_l),array("f",[l+max(lumi)*.001*n for l in lumi]),array("f",res_l))
        gu=ROOT.TGraph(len(res_l),array("f",[l+max(lumi)*.001*n for l in lumi]),array("f",res_u))
       
        g1.SetMarkerStyle(20)
        gl.SetMarkerStyle(22)
        gu.SetMarkerStyle(23)

        g1.SetName("cent_"+names[n])
        gl.SetName("lowlimit_"+names[n])
        gu.SetName("uplimit_"+names[n])
        
        for graph in [g1,gl,gu]:
            graph.SetMarkerColor(colors[n])
            graph.SetLineColor(colors[n])
            gp_cont.append(graph)
        leg.AddEntry(graph,names[n],"lp")
    c1=ROOT.TCanvas()
    gp_cont[0].SetMaximum(1.0)
    gp_cont[0].SetMinimum(0.0)
    gp_cont[0].Draw("apl")
    for graph in gp_cont[1:]:
        graph.Draw("pl")
    leg.Draw()
    out_rf=ROOT.TFile(options.out_file,"Recreate")
    out_rf.cd()
    for graph in gp_cont:
        graph.Write()
    c1.Write(options.out_file)
    out_rf.Write()
    out_rf.Close()
    # hists=[]
    # for hname in ["OOw","LRw","RRw","LLw","OLw","ORw"]:
    #     hists.append(rf.Get(hname))


    # mc=ROOT.TObjArray(len(hists))
    # for h in hists:
    #     mc.Add(h)
    # fit=ROOT.TFractionFitter(norm,mc)
    # for i in range(len(hists)):    
    #     fit.Constrain(i,0,1.0)
    # fit.Fit()



    # un_norm=unfold(norm)
    # fit_r=unfold(fit.GetPlot())
    # c1=ROOT.TCanvas()
    # fit_r.Draw("hist")

    # un_hists=[]
    # for h in hists:
    #     un_hists.append(unfold(h))


    # stack=ROOT.THStack()
    # for i,h in enumerate(un_hists):
    #     res=ROOT.Double()
    #     err=ROOT.Double()
    #     fit.GetResult(i,res,err)
    #     h.Scale(res*un_norm.Integral()*1./h.Integral()   )
    #     h.SetLineColor(colors[i])
    #     h.SetFillColor(colors[i])
    #     h.Draw("same")
    #     stack.Add(h)
    # stack.Draw("hist")
    # un_norm.Draw("same")

    # fit.Delete()
    # del fit

    # c2=ROOT.TCanvas()



#    mc1d=ROOT.TObjArray(len(hists))
#    for h in [h_O,h_L,h_R]:
#        mc1d.Add(h)




