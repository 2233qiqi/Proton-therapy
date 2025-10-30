#include "RunAction.hh"
#include "SteppingAction.hh"
#include "DetectorConstruction.hh"

#include "G4Run.hh"
#include "G4SystemOfUnits.hh"
#include <fstream>
#include <iomanip>
#include <iostream>
#include "TCanvas.h"
#include "TGraph.h"
#include "TAxis.h"
#include "TStyle.h"
#include "TROOT.h"


RunAction::RunAction()
    : fTotalEnergyDeposit(0.), fEventCount(0)
{}

RunAction::~RunAction() = default;

void RunAction::BeginOfRunAction(const G4Run* run)
{
    G4cout << " Run " << run->GetRunID() << " started." << G4endl;
    fTotalEnergyDeposit = 0.;
    fEventCount = 0;
    WriteDepthDose();  
}

void RunAction::EndOfRunAction(const G4Run* run)
{
    G4double avgEdep = fTotalEnergyDeposit / fEventCount;
    G4double detMass =SheildVolume;
    G4double dose = avgEdep / detMass;

    std::ofstream out("dose_output.txt", std::ios::app);
    out << std::fixed << std::setprecision(6)
        << run->GetRunID() << " "
        << dose / gray << G4endl;
    out.close();

    G4cout << "Run " << run->GetRunID() << " ended." << G4endl;
    G4cout << "  Total events: " << fEventCount << G4endl;
    G4cout << "  Average dose: " << dose / gray << " Sv" << G4endl;
    G4cout << "Total deposited energy in detector: "
       << fTotalEnergyDeposit / CLHEP::MeV << " MeV" << G4endl;

}

G4Run* RunAction::GenerateRun()
{
    return new G4Run();
}


void RunAction::WriteDepthDose()
{
    const auto& depthEdep = SteppingAction::GetDepthEdep();
    const G4int nBins = SteppingAction::GetNBins();
    const G4double maxDepth = SteppingAction::GetMaxDepth();

    if (depthEdep.empty() || nBins == 0 || maxDepth == 0) {
        G4cout << "Warning: Depth-dose data not initialized, skipping ROOT drawing." << G4endl;
        return;
    }

    TGraph* graph = new TGraph(nBins);

    for (int i = 0; i < nBins; ++i) {
        G4double depth = (i + 0.5) * (maxDepth / nBins);
        G4double edep = depthEdep[i];
        graph->SetPoint(i, depth / CLHEP::mm, edep / CLHEP::MeV);
    }

    gStyle->SetOptStat(0);
    TCanvas* c1 = new TCanvas("c1", "Depth Dose Distribution", 800, 600);
    c1->SetGrid();

    graph->SetTitle("Depth-Energy Deposition Distribution;Depth (mm);Deposited Energy (MeV)");
    graph->SetLineColor(kRed);
    graph->SetLineWidth(2);
    graph->SetMarkerStyle(20);
    graph->SetMarkerColor(kRed);

    graph->Draw("ALP");

    c1->SaveAs("depth_dose.root");
    c1->SaveAs("depth_dose.png");

    G4cout << "ROOT plot generated: depth_dose.root / depth_dose.png" << G4endl;
}
