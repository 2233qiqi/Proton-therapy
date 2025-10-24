#ifndef RunAction_h
#define RunAction_h 1

#include "G4UserRunAction.hh"
#include "globals.hh"
#include <vector>

class G4Run;

class RunAction : public G4UserRunAction
{
public:
    RunAction();
    ~RunAction() override;

    G4Run* GenerateRun() override;
    void BeginOfRunAction(const G4Run*) override;
    void EndOfRunAction(const G4Run*) override;
    void AddEnergyDeposit(G4double edep) { fTotalEnergyDeposit += edep; fEventCount++; }

private:
    void WriteDepthDose();  

    G4double fTotalEnergyDeposit;
    G4int    fEventCount;
};
#endif
