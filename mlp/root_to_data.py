import ROOT
import gzip
import sys
import random
import cPickle
from numpy import array

"""Usage: root_to_data input.root
This script reads in a root tree, and ouputs a pickled theano based array for training the MLP to ./data/WWdata_ct2.pkl.gz
"""

if __name__=="__main__":

      in_file=ROOT.TFile(sys.argv[1])

      input_vars=[
          "Lep_pt1","Lep_eta1",
          "Lep_phi1","Lep_pt2",
          "Lep_eta2","Lep_phi2",
          "Jet_pt1","Jet_eta1",
          "Jet_phi1", "Jet_pt2",
          "Jet_eta2","Jet_phi2",
          "MEt_Et","MEt_Phi"]

      target_vars=["ct1","ct2"]

      t=in_file.Get("Test")

      in_sets=[[],[],[]]
      tar_sets=[[],[],[]]

      for evt in xrange(t.GetEntries()     ):
          t.GetEntry(evt)
          input_v=[getattr(t,i) for i in input_vars]
          target_v=[getattr(t,i) for i in target_vars]
          set_int=random.randint(0,2)
          in_sets[set_int].append( input_v )
          tar_sets[set_int].append(target_v )

      train_set=(array(in_sets[0]),array(tar_sets[0]))
      valid_set=(array(in_sets[1]),array(tar_sets[1]))
      test_set=(array(in_sets[2]),array(tar_sets[2]))

      out=gzip.open("./data/WWdata_ct2.pkl.gz","wb")

      cPickle.dump([train_set,valid_set,test_set],out)
      out.close()


