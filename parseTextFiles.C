#include <iostream>
#include <fstream>
#include <vector>
#include <TString.h>
using namespace std;

//--------------------------
//    GLOBAL PARAMETERS
//--------------------------
struct sftxt {
  TString campaign;
  double etalow, etahigh;
  double ptlow, pthigh;
  double sfdown, sf, sfup;
};

std::vector<sftxt> muonIDSF, muonIsoSF;

//Function declarations:
void read_muon_sf();
double returnMuonIDSF(float pt, float eta, TString campaign, TString mode);
double returnMuonIsoSF(float pt, float eta, TString campaign, TString mode);

//___________________________________________________________________________________________________
//
// Main
//___________________________________________________________________________________________________

void parseTextFiles() {

  //Initialise global paramters.
  read_muon_sf();

  //The following can be done in event loops.
  float   testPt = 22.0;
  float   testEta = 0.5;
  TString testCampaign = "2016postVFP_UL";

  double sfdown, sf, sfup;

  cout<<"\nTest scale factor for muons:"<<endl;
  cout<<"For pT = "<<testPt<<", eta = "<<testEta<<" and campaign = "<<testCampaign<<" :"<<endl;
  
  sf     = returnMuonIDSF(testPt, testEta, testCampaign, "nom");
  sfup   = returnMuonIDSF(testPt, testEta, testCampaign, "systup");
  sfdown = returnMuonIDSF(testPt, testEta, testCampaign, "systdown");
  cout<<"ID scale factors (down, nom, up) = "<<sfdown<<", "<<sf<<", "<<sfup<<endl;

  sf     = returnMuonIsoSF(testPt, testEta, testCampaign, "nom");
  sfup   = returnMuonIsoSF(testPt, testEta, testCampaign, "systup");
  sfdown = returnMuonIsoSF(testPt, testEta, testCampaign, "systdown");
  cout<<"Isolation scale factors (down, nom, up) = "<<sfdown<<", "<<sf<<", "<<sfup<<endl;
  
  /*
  cout << "Printing all entries in muonIsoSF:" << endl;
  for (const auto& entry : muonIsoSF) {
    cout << "Campaign: " << entry.campaign
	 << " | eta range: " << entry.etalow << " - " << entry.etahigh
	 << " | pt range: " << entry.ptlow << " - " << entry.pthigh
	 << " | SFdown: " << entry.sfdown
	 << " | SF: " << entry.sf
	 << " | SFup: " << entry.sfup << endl;
	 }*/
  
  cout<<"\nSuccess!\n"<<endl;

}

//___________________________________________________________________________________________________
//
// Function definitions
//___________________________________________________________________________________________________

void read_muon_sf() {
  
  TString txt_muon_id_sf = "corrections/muonsf/muon_id_sf.txt";
  ifstream infile(txt_muon_id_sf.Data());
  sftxt entry;
  while (infile >> entry.campaign
	 >> entry.etalow >> entry.etahigh
	 >> entry.ptlow  >> entry.pthigh
	 >> entry.sfdown >> entry.sf >> entry.sfup) {
    muonIDSF.push_back(entry);
  }
  infile.close();
  
  TString txt_muon_iso_sf = "corrections/muonsf/muon_iso_sf.txt";
  ifstream infile1(txt_muon_iso_sf.Data());
  sftxt entry1;
  while (infile1 >> entry1.campaign
	 >> entry1.etalow >> entry1.etahigh
	 >> entry1.ptlow  >> entry1.pthigh
	 >> entry1.sfdown >> entry1.sf >> entry1.sfup) {
    muonIsoSF.push_back(entry1);
  }
  infile1.close();

  cout<<"Muon correction factors loaded."<<endl;
}

double returnMuonIDSF(float pt, float eta, TString campaign, TString mode){
  for(const auto& entry : muonIDSF) {
    bool campaign_match = entry.campaign == campaign;
    bool in_pteta_range = (entry.etalow <= eta && eta < entry.etahigh) && 
                          (entry.ptlow  <= pt  && pt  < entry.pthigh);
    if(campaign_match){
      if(in_pteta_range){
        if (mode == "nom")           return entry.sf;
        else if (mode == "systup")   return entry.sfup;
        else if (mode == "systdown") return entry.sfdown;
        else {
          cout << "Error: Unknown mode: " << mode <<endl;
          return 1.0;
        }
      }
      else continue;
    }
  }

  // If no campaign matches or no range matches after the loop, return -1.0
  cout << "Error: No matching campaign or range found for pt=" << pt << ", eta=" << eta << ", campaign=" << campaign << endl;
  return -1.0;
}

double returnMuonIsoSF(float pt, float eta, TString campaign, TString mode){
  for(const auto& entry : muonIsoSF) {
    bool campaign_match = entry.campaign == campaign;
    bool in_pteta_range = (entry.etalow <= eta && eta < entry.etahigh) && 
                          (entry.ptlow  <= pt  && pt  < entry.pthigh);
    if(campaign_match){
      if(in_pteta_range){
        if (mode == "nom")           return entry.sf;
        else if (mode == "systup")   return entry.sfup;
        else if (mode == "systdown") return entry.sfdown;
        else {
          cout << "Error: Unknown mode: " << mode <<endl;
          return 1.0;
        }
      }
      else continue;
    }
  }

  // If no campaign matches or no range matches after the loop, return -1.0
  cout << "Error: No matching campaign or range found for pt=" << pt << ", eta=" << eta << ", campaign=" << campaign << endl;
  return -1.0;
}
