#include "RunAction.hh"
#include "SteppingAction.hh" 
#include "DetectorConstruction.hh" 

#include "G4Run.hh"
#include "G4SystemOfUnits.hh"
#include <fstream>
#include <iomanip>

#include "TCanvas.h"
#include "TGraph.h"
#include "TStyle.h"


RunAction::RunAction(const DetectorConstruction* det)
    : fDetConstruction(det), fTotalEnergyDeposit(0.), fEventCount(0)
{}

RunAction::~RunAction() = default;


G4Run* RunAction::GenerateRun()
{
    return new G4Run();
}

void RunAction::AddTotalEnergyAndCount(G4double edep)
{
    fTotalEnergyDeposit += edep;
    fEventCount++;
}

void RunAction::BeginOfRunAction(const G4Run* run)
{
    fTotalEnergyDeposit = 0.;
    fEventCount = 0;
}

void RunAction::EndOfRunAction(const G4Run* run)
{
    G4int totalEvents = run->GetNumberOfEvent();

    G4cout << "penetrate event: " << fEventCount << G4endl; 
    
    if (totalEvents == 0) return; 

    G4double detMass = 0.0;
    if (fDetConstruction) {
        detMass = fDetConstruction->GetDetectorMass(); 
    }
    
    if (detMass <= 0.0) {
        G4cerr << " Dose calculation failed." << G4endl;
        return;
    }

    G4double avgEdep_perEvent_Joule = fTotalEnergyDeposit / (G4double)totalEvents; 
    
    G4double dose = fTotalEnergyDeposit / (CLHEP::joule * (G4double)totalEvents * detMass); 
    
    G4cout << "detmass: " << detMass <<" kg"<< G4endl; 

    G4double dose_gy = dose / CLHEP::gray;
    
    std::ofstream out("dose_output.txt", std::ios::app);
    out << std::fixed << std::setprecision(15)
        << run->GetRunID() << " "
        << dose_gy << G4endl; 
    out.close();

    G4cout << "Run " << run->GetRunID() << " ended. Dose: " << dose_gy << " Gy" << G4endl;
}

