#include "RunAction.hh"
#include "G4Run.hh"
#include "G4SystemOfUnits.hh"
#include <fstream>
#include <iomanip>

RunAction::RunAction()
    : fTotalEnergyDeposit(0.), fEventCount(0)
{}

RunAction::~RunAction() = default;

void RunAction::BeginOfRunAction(const G4Run* run)
{
    G4cout << " Run " << run->GetRunID() << " started." << G4endl;
    fTotalEnergyDeposit = 0.;
    fEventCount = 0;
}

void RunAction::EndOfRunAction(const G4Run* run)
{
 
    G4double avgEdep = fTotalEnergyDeposit / fEventCount;//计算平均能量

  
    G4double detMass = 40.0 * g; 
    G4double dose = avgEdep / detMass; 

   
    std::ofstream out("dose_output.txt", std::ios::app);
    out << std::fixed << std::setprecision(6)
        << run->GetRunID() << " "
        << dose / gray << " "  
        << G4endl;
    out.close();

    G4cout << "Run " << run->GetRunID() << " ended." << G4endl;
    G4cout << "  Total events: " << fEventCount << G4endl;
    G4cout << "  Average dose: " << dose / gray << " Gy" << G4endl;
}