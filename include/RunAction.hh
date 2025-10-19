#ifndef RUNACTION_HH
#define RUNACTION_HH

#include "G4UserRunAction.hh"
#include "G4Run.hh"
#include "G4VAnalysisManager.hh"
#include "DetectorConstruction.hh"


class RunAction : public G4UserRunAction
{
public:

    RunAction(DetectorConstruction *dec, G4VAnalysisManager* man);
    

    virtual ~RunAction() override; 
    
    G4Run *GenerateRun() override;

    void BeginOfRunAction(const G4Run *) override;
    void EndOfRunAction(const G4Run*) override;

private:

    DetectorConstruction* fDetConstruction;
    void ReadAndWriteDose(const G4Run* run);
};

#endif
