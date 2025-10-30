// RunAction.hh (修正后)

#ifndef RunAction_h
#define RunAction_h 1

#include "G4UserRunAction.hh"
#include "globals.hh"
#include "DetectorConstruction.hh" // 必须包含 DetectorConstruction 的头文件
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
    
    void AddEnergyDeposit(G4double edep) { fTotalEnergyDeposit += edep; }

private:
    void WriteDepthDose(G4double doseValue, G4int runID); 
    
    const DetectorConstruction* fDetConstruction; 
    G4double fTotalEnergyDeposit = 0.0; 
    G4int fEventCount = 0; 

};
#endif