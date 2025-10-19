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


