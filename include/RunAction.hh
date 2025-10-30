#ifndef RunAction_h
#define RunAction_h 1

#include "G4UserRunAction.hh"
#include "globals.hh"
#include "DetectorConstruction.hh"
#include <vector>

class G4Run;

class RunAction : public G4UserRunAction
{
public:
    RunAction(const DetectorConstruction* det); 
    ~RunAction() override;

    G4Run* GenerateRun() override;
    void BeginOfRunAction(const G4Run*) override;
    void EndOfRunAction(const G4Run*) override;


    void AddTotalEnergyAndCount(G4double edep);


private:


    const DetectorConstruction* fDetConstruction;

    G4double fTotalEnergyDeposit = 0.0;
    G4int fEventCount = 0;
};

#endif
