import ROOT

rf=ROOT.TFile("TMVA_out.root")
TestTree=rf.Get("TestTree")

TestTree.Draw("BDT>>OO(20,0,.25)","OOw","norm")
TestTree.Draw("BDT>>TO(20,0,.25)","TOw","same norm")
TestTree.Draw("BDT>>TT(20,0,.25)","TTw","same norm")

TestTree.Draw("BDT>>LL(20,0,.25)","LLw","same norm")
TestTree.Draw("BDT>>RR(20,0,.25)","RRw","same norm")
TestTree.Draw("BDT>>LR(20,0,.25)","LRw","same norm")

TestTree.Draw("BDT>>OL(20,0,.25)","OLw","same norm")
TestTree.Draw("BDT>>OR(20,0,.25)","ORw","same norm")

ROOT.OO.Draw()
ROOT.TO.Draw("same")
ROOT.TT.Draw("same")

ROOT.OR.Draw("same")
ROOT.OL.Draw("same")
ROOT.RR.Draw("same")

ROOT.LL.Draw("same")
ROOT.LR.Draw("same")
