#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TAxis.h>
#include <TLegend.h>
#include <TPad.h>
#include <TLine.h>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <cmath>

using namespace std;

struct SFData {
    vector<double> pt;
    vector<double> pt_err;
    vector<double> sf;
    vector<double> err_low;
    vector<double> err_up;
};

struct SFContainer {
    map<pair<double, double>, map<TString, SFData>> data;
};

struct CampaignInfo {
    map<TString, int> colors = {
        {"2016postVFP_UL", kRed},
        {"2016preVFP_UL", kBlue},
        {"2017_UL", kGreen},
        {"2018_UL", kMagenta},
        {"Run3Summer22", kCyan},
        {"Run3Summer22EE", kOrange},
        {"Run3Summer23", kViolet},
        {"Run3Summer23BPix", kBlack}
    };
};

SFContainer loadData(TString infile) {
    ifstream file(infile.Data());
    SFContainer container;
    string line;
    
    while (getline(file, line)) {
        istringstream iss(line);
        TString campaign;
        double eta_min, eta_max, pt_min, pt_max, phi_min, phi_max, sfdown, sf, sfup;
        
        iss >> campaign >> eta_min >> eta_max >> pt_min >> pt_max >> phi_min >> phi_max >> sfdown >> sf >> sfup;
        
        auto &sfData = container.data[{eta_min, eta_max}][campaign];
        sfData.pt.push_back((pt_min + pt_max) / 2.0);
        sfData.pt_err.push_back((pt_max - pt_min) / 2.0);
        sfData.sf.push_back(sf);
        sfData.err_low.push_back(sf - sfdown);
        sfData.err_up.push_back(sfup - sf);
    }
    
    return container;
}

void decorateGraph(TGraphErrors* graph) {
    graph->SetMarkerStyle(20);
    graph->SetMarkerSize(0.7);
    graph->SetLineWidth(1);
    graph->GetXaxis()->SetTitle("pT (GeV)");
    graph->GetXaxis()->SetTitleSize(0.10);
    graph->GetXaxis()->SetTitleOffset(1.15);
    graph->GetXaxis()->SetLabelSize(0.10);
    graph->GetYaxis()->SetTitle("SF");
    graph->GetYaxis()->SetRangeUser(0, 2);
    graph->GetYaxis()->SetTitleSize(0.13);
    graph->GetYaxis()->SetTitleOffset(0.28);
    graph->GetYaxis()->SetLabelSize(0.08);
    graph->GetYaxis()->SetNdivisions(505);
}

void plotSF(TString correctionName, TString inputFile) {
  SFContainer container = loadData(inputFile);
  CampaignInfo campaignInfo;
  int nPads = container.data.size();
  int nCols = 2;
  int nRows = ceil(nPads / (double)nCols);
    
  auto c1 = new TCanvas("c1", correctionName, 1200, 800);
  c1->Divide(nCols, nRows, 0.001, 0.001);
    
  int padIndex = 1;
  for (auto &[eta_range, campaigns] : container.data) {
    c1->cd(padIndex);
    auto pad = gPad;
    float rightmargin  = 0.25;
    float bottommargin = 0.25;
    pad->SetBottomMargin(bottommargin);
    pad->SetRightMargin(rightmargin);
    pad->SetLogx(1);
    auto legend = new TLegend(1-rightmargin+0.01, bottommargin, 0.98, 0.9);
    legend->SetBorderSize(0);
    legend->SetTextSize(0.06);
        
    double xmin = 10, xmax = 1500;
    auto line = new TLine(xmin, 1.0, xmax, 1.0);
    line->SetLineStyle(1);
    line->SetLineWidth(2);
    line->SetLineColor(kRed);
    line->Draw();
        
    for (auto &[campaign, sfData] : campaigns) {
      if (campaignInfo.colors.find(campaign) == campaignInfo.colors.end()) continue;
            
      int n = sfData.pt.size();
      auto graph = new TGraphErrors(n, sfData.pt.data(), sfData.sf.data(), sfData.pt_err.data(), sfData.err_up.data());
      graph->SetMarkerColor(campaignInfo.colors[campaign]);
      graph->SetLineColor(campaignInfo.colors[campaign]);
      graph->SetTitle("");
      decorateGraph(graph);
            
      if (legend->GetNRows() == 0) graph->Draw("AP");
      else graph->Draw("P SAME");
            
      legend->AddEntry(graph, campaign, "p");
    }
        
    auto text = new TLatex(1-rightmargin-0.01, 1-bottommargin+0.05, Form("%.1f < #eta < %.1f", eta_range.first, eta_range.second));
    text->SetNDC();
    text->SetTextAlign(31);
    text->SetTextSize(0.07);
    text->Draw();
        
    legend->Draw();
        
    padIndex++;
  } 
}

void plotCorrections() {
    plotSF("Electron ID SF", "corrections/electronsf/electron_id_sf.txt");
}
