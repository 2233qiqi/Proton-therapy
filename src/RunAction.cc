#include "RunAction.hh"
#include "SteppingAction.hh"

#include "G4Run.hh"
#include "G4SystemOfUnits.hh"
#include <fstream>
#include <iomanip>
#include <iostream>

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
    G4double detMass = 40.0 * g;
    G4double dose = avgEdep / detMass;

    std::ofstream out("dose_output.txt", std::ios::app);
    out << std::fixed << std::setprecision(6)
        << run->GetRunID() << " "
        << dose / gray << G4endl;
    out.close();

    G4cout << "Run " << run->GetRunID() << " ended." << G4endl;
    G4cout << "  Total events: " << fEventCount << G4endl;
    G4cout << "  Average dose: " << dose / gray << " Gy" << G4endl;
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

    if (depthEdep.empty() || nBins == 0 || maxDepth == 0)
    {
        G4cout << "Warning: Depth-dose data not initialized, skipping output." << G4endl;
        return;
    }

    std::ofstream outFile("depth_dose.txt");
    for (int i = 0; i < nBins; ++i)
    {
        G4double depth = (i + 0.5) * (maxDepth / nBins);
        outFile << std::setw(10) << depth / CLHEP::mm << " "
                << std::setw(14) << depthEdep[i] / CLHEP::MeV << "\n";
    }
    outFile.close();

    G4cout << "Depth-dose data written to depth_dose.txt" << G4endl;
}
