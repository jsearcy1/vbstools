import ROOT
import sys

rf1=ROOT.TFile(sys.argv[1])
rf2=ROOT.TFile(sys.argv[2])
var=sys.argv[3]
var1=var+"1"
var2=var+"2"

t1=rf1.Get("Test")
t2=rf2.Get("Test")

diff=ROOT.TH1F("Diff","Diff",100,-100,100)
#miss=ROOT.TH1F("Missing","Missing",100,-5,5)
miss=ROOT.TH1F("Missing","Missing",100,0,500)
all_v=miss.Clone()
kill=0
nevt=t1.GetEntries()
if t2.GetEntries()!=nevt:
    print "Bad samples"
    sys.exit()

for evt in range(nevt):
    t1.GetEntry(evt)
    t2.GetEntry(evt)

    value1_file1=getattr(t1,var1)
    value2_file1=getattr(t1,var2)

    value1_file2=getattr(t2,var1)
    value2_file2=getattr(t2,var2)

    if t1.Lep_pt1 <10 or t1.Lep_pt2 < 10:continue
    if abs(t1.Lep_eta1) >2.5 or abs(t1.Lep_eta2) > 2.5:continue

    all_v.Fill(value1_file1)
    all_v.Fill(value2_file1)
    if value1_file2==0 and value2_file2==0:
        kill+=1

        miss.Fill(value1_file1)
        miss.Fill(value2_file1)
    elif value1_file2!=0 and value2_file2 !=0:
        if  (value1_file2-value1_file1)**2+(value2_file2-value2_file1)**2 < (value1_file2-value2_file1)**2+(value2_file2-value1_file1)**2:
            diff.Fill(value1_file2-value1_file1)
            diff.Fill(value2_file2-value2_file1)
        else:
            diff.Fill(value1_file2-value2_file1)
            diff.Fill(value2_file2-value1_file1)
    elif value1_file2==0:
        kill+=1

        if(abs(value2_file2-value2_file1) < abs(value2_file2-value1_file1)):
            diff.Fill(value2_file2-value2_file1)
            miss.Fill(value1_file1)
        else:
            diff.Fill(value2_file2-value1_file1)
            miss.Fill(value2_file1)
    elif value2_file2==0:
        kill+=1

        if(abs(value1_file2-value2_file1) < abs(value1_file2-value1_file1)):
            diff.Fill(value1_file2-value2_file1)
            miss.Fill(value1_file1)
        else:
            diff.Fill(value1_file2-value1_file1)
            miss.Fill(value2_file1)

found=all_v.Clone()
found.Add(miss,-1)
eff=found.Clone()
eff.Divide(all_v)


#Since these get mixed up we need to make sure we get the corret pair

       

    
    
