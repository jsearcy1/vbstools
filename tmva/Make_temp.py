import ROOT
from array import array
rand=ROOT.TRandom()

class classifier():
    def __init__(self):
        self.input_vars=[
            "Lep_pt1","Lep_eta1",
            "Lep_phi1","Lep_pt2",
            "Lep_eta2","Lep_phi2",
            "Jet_pt1","Jet_eta1",
            "Jet_phi1", "Jet_pt2",
            "Jet_eta2","Jet_phi2",
            "MEt_Et","MEt_Phi"]
        self.var_dict={}
        for i in self.input_vars:
            self.var_dict[i]=array("f",[0])

        self.reader=ROOT.TMVA.Reader();
        for i in self.input_vars: ##need to use input_vars here instead of var_dict because it turns out the order is important
            self.reader.AddVariable(i,self.var_dict[i])
        self.reader.BookMVA("BDT","weights/MVAnalysis_BDT.weights.xml")    

    def Value(self):
        return self.reader.EvaluateMVA( "BDT" )

    def set_variables(self,t):
        for i in self.var_dict:
            self.var_dict[i][0]=getattr(t,i)


in_rf=ROOT.TFile("Output_sm_fixed.root")
t=in_rf.Get("Test")

BDT_h=ROOT.TH1F("bdt","bdt",30,0,.3)
BDT_TT=BDT_h.Clone()
BDT_TL=BDT_h.Clone()
BDT_LL=BDT_h.Clone()


BDT=classifier()
jet1=ROOT.TLorentzVector()
jet2=ROOT.TLorentzVector()
for evt in xrange(t.GetEntries()):
    t.GetEntry(evt)
    BDT.set_variables(t)
    val=BDT.Value()

    jet1.SetPtEtaPhiM(t.Jet_pt1,t.Jet_eta1,t.Jet_phi1,0)
    jet2.SetPtEtaPhiM(t.Jet_pt2,t.Jet_eta2,t.Jet_phi2,0)

    mjj=(jet1+jet2).M()
    if mjj < 500:continue
    if abs(jet1.Rapidity()-jet2.Rapidity()) < 2.4:continue    
    BDT_h.Fill(val)    
    BDT_TT.Fill(val,t.TTw)
    BDT_TL.Fill(val,t.TOw)
    BDT_LL.Fill(val,t.OOw)
    

BDT_h.Scale(3.13/BDT_h.Integral()) #1 fb worth of 13 TeV data

out_rf=ROOT.TFile("temps_out.root","Recreate")
out_rf.cd()
BDT_h.SetName("BDT_h")
BDT_TT.SetName("BDT_TT")
BDT_TL.SetName("BDT_TL")
BDT_LL.SetName("BDT_LL")
BDT_h.Write()
BDT_TT.Write()
BDT_TL.Write()
BDT_LL.Write()
out_rf.Write()
out_rf.Close()
