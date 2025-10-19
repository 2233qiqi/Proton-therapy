#ifndef RUNACTION_HH
#define RUNACTION_HH

#include "G4UserRunAction.hh"
#include "G4Run.hh"
#include "G4VAnalysisManager.hh"
#include "DetectorConstruction.hh"
#include "string"


class RunAction : public G4UserRunAction
{
public:

RunAction(DetectorConstruction *dec,G4VAnalysisManager* man);
G4Run *GenerateRun();
virtual void BeginOfRunAction(const G4Run *);
virtual void EndOfRunAction(const G4Run*);

private:

DetectorConstruction* fDetConstruction;
void ReadAndWriteDose(const G4Run* run);


};

#endif