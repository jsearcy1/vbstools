import ROOT
out_rf=ROOT.TFile("TMVA_out.root","Recreate")
fac=ROOT.TMVA.Factory("MVAnalysis", out_rf,"!V:Transformations=I;N;D")
rf_in=ROOT.TFile("Output_sm.root")

t=rf_in.Get("Test")
fac.AddRegressionTree(t)
for n in t.GetListOfBranches():
    if (n.GetName() not in ["RRw","LRw","LLw","target",
                            "TOw","OOw","ORw","OLw","TTw",
                            "ct1","ct2","Mww"]
        and "Nu" not in n.GetName()):

        print n.GetName()
        #if "Jet" in n.GetName():
        fac.AddVariable(n.GetName(),"F")
    else:
        fac.AddSpectator(n.GetName(),"F")

#fac.AddTarget("TTw")
#fac.AddTarget("TLw")
#fac.AddTarget("LLw")
fac.AddTarget("OOw")

#fac.PrepareTrainingAndTestTree(ROOT.TCut(""),10000,10000,10000,10000)

fac.BookMethod(ROOT.TMVA.Types.kBDT,"BDT","SeparationType=RegressionVariance:NTrees=100")   
#fac.BookMethod( ROOT.TMVA.Types.kMLP, "MLP", "!H:!V:VarTransform=Norm:NeuronType=tanh:NCycles=20000:HiddenLayers=N+20:TestRate=6:TrainingMethod=BFGS:Sampling=0.3:SamplingEpoch=0.8:ConvergenceImprovsise=1e-6:ConvergenceTests=15:!UseRegulator" );

#fac.BookMethod( ROOT.TMVA.Types.kSVM, "SVM", "Gamma=0.25:Tol=0.001:VarTransform=Norm" );
#fac.BookMethod( ROOT.TMVA.Types.kBDT, "BDTG",
#                "!H:!V:NTrees=20.BoostType=Grad:Shrinkage=0.1:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:MaxDepth=20:NNodesMax=20" );
# fac.BookMethod( ROOT.TMVA.Types.kFDA, "FDA_GAMT",
#                 "!H:!V:Formula=(0)+(1)*x0+(2)*x1:ParRanges=(-100,100);(-100,100);(-100,100):FitMethod=GA:Converger=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=0:!UseImprove:!UseMinos:SetBatch:Cycles=1:PopSize=5:Steps=5:Trim" )
# fac.BookMethod( ROOT.TMVA.Types.kFDA, "FDA_MT",                                                   
#                 "!H:!V:Formula=(0)+(1)*x0+(2)*x1:ParRanges=(-100,100);(-100,100);(-100,100);(-10,10):FitMethod=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=2:UseImprove:UseMinos:SetBatch" );
# fac.BookMethod( ROOT.TMVA.Types.kFDA, "FDA_GA",
#                 "!H:!V:Formula=(0)+(1)*x0+(2)*x1:ParRanges=(-100,100);(-100,100);(-100,100):FitMethod=GA:PopSize=100:Cycles=3:Steps=30:Trim=True:SaveBestGen=1:VarTransform=Norm" );
# fac.BookMethod( ROOT.TMVA.Types.kFDA, "FDA_MC",
#                 "!H:!V:Formula=(0)+(1)*x0+(2)*x1:ParRanges=(-100,100);(-100,100);(-100,100):FitMethod=MC:SampleSize=100000:Sigma=0.1:VarTransform=D" );
# fac.BookMethod( ROOT.TMVA.Types.kLD, "LD", 
#                 "!H:!V:VarTransform=None" );
# fac.BookMethod( ROOT.TMVA.Types.kKNN, "KNN", 
#                 "nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim" );
#fac.BookMethod( ROOT.TMVA.Types.kPDEFoam, "PDEFoam", 
#                "!H:!V:MultiTargetRegression=F:TargetSelection=Mpv:TailCut=0.001:VolFrac=0.0666:nActiveCells=500:nSampl=2000:nBin=5:Compress=T:Kernel=None:Nmin=10:VarTransform=None" );

#fac.BookMethod( ROOT.TMVA.Types.kPDERS, "PDERS", 
#                "!H:!V:NormTree=T:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=40:NEventsMax=60:VarTransform=None" );

fac.PrepareTrainingAndTestTree(ROOT.TCut(""),"nTrain_Regression=100000:nTest_Regression=10000")

fac.TrainAllMethods()  
fac.TestAllMethods()
fac.EvaluateAllMethods()
