//<A simple program to slim Root tree header>

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include <TSelector.h>
#include <TROOT.h>
#include <TDirectory.h>
#include <vector>
#include <stdlib.h>

#ifdef __MAKECINT__
#pragma link C++ class vector<float>+;
#endif

using namespace std;

int convert(string inputlist="input_list.txt") {
  
  int npar; // n particles
  vector<int> pid; vector<int> pstatus; vector<int> pmother1; vector<int> pmother2;
  vector<int> pcolor1; vector<int> pcolor2; vector<int> pspin;
  float evt_wt, evt_scale, evt_aem, evt_aqcd; //event weight/scale
  //four momentum
  vector<float> ppx; vector<float> ppy; vector<float> ppz; vector<float> pE; vector<float> pM;
  vector<float> plife; //life time
  
  ifstream filelist;
  //list of lhe files
  filelist.open(inputlist.c_str());
  if(!filelist.good()) {
    cout<<"ERROR: Cannot find the input filelist, now quit!"<<endl;
    exit(-1);
  }
  
  int nroot = 0;
  char buf[100];
  string line;
  while(!filelist.eof()){
    //read each lhe file
    getline(filelist,line);
    if(line.size()==0) continue;
    
    size_t found = line.find_last_of("/\\");
    string output = line.substr(found+1);
    nroot ++; sprintf(buf, "%d", nroot);
    string _output=output+".2"+buf+".root";
    TFile *fout = new TFile(_output.c_str(), "RECREATE");
    TTree *lhe = new TTree("truth", "truth");

    //define branches
    lhe->Branch("p_px", &ppx); 
    lhe->Branch("p_py", &ppy); 
    lhe->Branch("p_pz", &ppz); 
    lhe->Branch("p_E", &pE); 
    lhe->Branch("p_M", &pM);
    
    lhe->Branch("npar", &npar); lhe->Branch("evt_weight", &evt_wt); lhe->Branch("evt_scale", &evt_scale);
    lhe->Branch("evt_alpha_em", &evt_aem); lhe->Branch("evt_alpha_qcd", &evt_aqcd);
    lhe->Branch("p_id", &pid); lhe->Branch("p_status", &pstatus);
    lhe->Branch("p_mother1", &pmother1); lhe->Branch("p_mother2", &pmother2);
    lhe->Branch("p_color1", &pcolor1); lhe->Branch("p_color2", &pcolor2);
    lhe->Branch("p_lifetime", &plife); lhe->Branch("p_spin", &pspin);	
    
    ifstream file;
    file.open(line.c_str());
    if(!file.good()) {
      cout<<"ERROR: Cannot find the input file: "<<line<<endl;
      exit(-1);
    } else { cout <<"INFO => Read lhe file: " <<line<<endl; }
    int nevt = 0;
    while(!file.eof()) {
      //read each line of the lhe file
      getline(file,line);        
      if(line.size()==0) continue; //remove the blank lines
      
      //clear the vectors 
      pid.clear(); pstatus.clear(); pmother1.clear(); pmother2.clear();
      pcolor1.clear(); pcolor2.clear(); pspin.clear();
      ppx.clear(); ppy.clear(); ppz.clear(); pE.clear(); pM.clear(); plife.clear();		
      
      //begin of each event: <event> ... </event>
      if(line.find("<event>") != string::npos) {
	getline(file,line);
	if(line.size()==0) continue;
	if(line.find("</event>") != string::npos) continue;
	nevt ++;
	if( nevt % 1000 == 0) cout << "Events converted: " << nevt << endl;
	istringstream iss(line);
	string s;
	vector<string> sline;
	//event line
	//split the line with space
	while( getline(iss, s, ' ') ) {
	  if(s.size()==0) continue;
	  else sline.push_back(s);
	}
	//the event line has 6 items
	if(sline.size()==0 || sline.size()!=6) continue;
	npar = atoi(sline[0].c_str()); evt_wt = float(atof(sline[2].c_str())); evt_scale = float(atof(sline[3].c_str()));
	evt_aem = float(atof(sline[4].c_str())); evt_aqcd = float(atof(sline[5].c_str()));
	//n particles in each event
	for( int i=0; i<npar; i++ ) {
	  getline(file,line);
	  if(line.size()==0) continue;
	  if(line.find("</event>") != string::npos) continue;
	  istringstream iss(line);
	  string s;
	  vector<string> sline;
	  //split the line with space
	  while( getline(iss, s, ' ') ) {
	    if(s.size()==0) continue;
	    else sline.push_back(s);
	  }
	  //the particle line has 13 items
	  if(sline.size()==0 || sline.size()!=13) continue;	
	  pid.push_back(atoi(sline[0].c_str())); pstatus.push_back(atoi(sline[1].c_str())); pmother1.push_back(atoi(sline[2].c_str())); pmother2.push_back(atoi(sline[3].c_str()));
	  pcolor1.push_back(atoi(sline[4].c_str())); pcolor2.push_back(atoi(sline[5].c_str()));
	  ppx.push_back(float(atof(sline[6].c_str()))); ppy.push_back(float(atof(sline[7].c_str()))); ppz.push_back((float(atof(sline[8].c_str())))); pE.push_back((float(atof(sline[9].c_str())))); pM.push_back((float(atof(sline[10].c_str()))));
	  plife.push_back((float(atof(sline[11].c_str())))); pspin.push_back(atoi(sline[12].c_str()));
	}
	lhe->Fill();
      }
    }
    fout->Write(0, TObject::kOverwrite);
    fout->Close();
  }
  
  return 0;	
}

// main code
int main(int argc, char *argv[]) {
  gROOT->ProcessLine("#include <vector>");
  
  if(argc==1) convert();
  else if(argc==2) convert(argv[1]);
  else cout<<"Error => Can not have so many arguments!!! "<<argc-1<<endl;
  return 0;
}
