import ROOT
import cPickle
from glob import glob
import os

pkfiles=glob("tests/test_output/*.pk")
dicts={}
for f in pkfiles:
    dicts[ os.path.split(f)[-1] ]=cPickle.load(open(f))

def Print(f):
    string=""
    for temp in ["TT","OT","OOw"]:
        vals=[i for i in dicts[f][temp] if i["lumi"]==3000][0]
    
        string+= str(round(vals["68"][0],2))+" & "+str(round(vals["68"][1],2))+" &"
    string=string.strip("& ")
    string+= "\\\\ \n"
    print string,

def Print2(f):
    string=""
    for temp in ["nOO","OOw"]:
        vals=[i for i in dicts[f][temp] if i["lumi"]==3000][0]
    
        string+= str(round(vals["68"][0],3))+" & "+str(round(vals["68"][1],3))+" &"
    string=string.strip("& ")
    string+= "\\\\ \n"
    print string,



print "\\begin{tabular}{c |cc|cc|cc}"
print "\hline"
print "Templates & \multicolumn{2}{c|}{TT} & \multicolumn{2}{c|}{OT}  & \multicolumn{2}{c}{OO} \\\\"
print "\hline"
print " & LL & UL & LL & UL & LL & UL  \\\\"
print "\hline"
print "Parton &",
Print("parton.root_1.pk")
print "ATLAS Cuts Parton &",
Print("parton_cuts_1.root_1.pk")
print "Delphes &",
Print("delphes.root_1.pk")
print "ATLAS Cuts Delphes &",
Print("delphes_cuts_1.root_1.pk")
print "\hline"
print "\hline"
print "\\end{tabular}"



print "\\begin{tabular}{c |cc|cc}"
print "\hline"
print "Templates & \multicolumn{2}{c|}{!OO} & \multicolumn{2}{c}{OO} \\\\"
print "\hline"
print " & LL & UL & LL & UL  \\\\"
print "\hline"
print "Parton &",
Print2("parton.root_2.pk")
print "ATLAS Cuts Parton &",
Print2("parton_cuts_1.root_2.pk")
print "Delphes &",
Print2("delphes.root_2.pk")
print "ATLAS Cuts Delphes &",
Print2("delphes_cuts_1.root_2.pk")
print "\hline"
print "\hline"
print "\\end{tabular}"
