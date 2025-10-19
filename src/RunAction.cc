#include "RunAction.hh"
#include "G4THitsMap.hh"
#include "G4UnitsTable.hh"
#include "DetectorConstruction.hh"

#include <iostream>
#include <fstream>
#include <iomanip>
#include <numeric>

RunAction::RunAction(DetectorConstruction* dec, G4VAnalysisManager* man)
: G4UserRunAction(),
  fDetConstruction(dec)
{

}

RunAction::~RunAction()
{}

G4Run* RunAction::GenerateRun()
{
    return G4UserRunAction::GenerateRun();
};

void RunAction::BeginOfRunAction(const G4Run*run)
{
   
    if (IsMaster()) 
    {
        ReadAndWriteDose(run);
    }
}

void RunAction::EndOfRunAction(const G4Run* run)
{
   
    if (IsMaster()) 
    {
        ReadAndWriteDose(run);
    }
}

void RunAction::ReadAndWriteDose(const G4Run* run)
{
    std::ofstream outfile("dose_output.txt", std::ios::app);
    if (!outfile.is_open()) {
        G4cerr << "无法打开输出文件 dose_output.txt" << G4endl;
        return;
    }

    G4int nEvents = run->GetNumberOfEvent();
    outfile << "Run " << run->GetRunID() << " 共 " << nEvents << " 个事件\n";

    outfile.close();
}

