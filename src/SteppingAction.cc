#include "SteppingAction.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4VProcess.hh"
#include "G4StepPoint.hh"


SteppingAction::SteppingAction()
: G4UserSteppingAction()
{
}


SteppingAction::~SteppingAction()
{
}


void SteppingAction::UserSteppingAction(const G4Step* aStep)
{
    
    G4Track* track = aStep->GetTrack();
    
 
    G4double edep = aStep->GetTotalEnergyDeposit();
    G4double stepl = aStep->GetStepLength();
    

    const std::vector<const G4Track*>* secondary = aStep->GetSecondaryInCurrentStep();
    if (secondary->size() > 0) 
    {
        // 可以在这里进行日志记录或统计
        // G4cout << "Step: Secondary particle created: " << (*secondary)[0]->GetDefinition()->GetParticleName() << G4endl;
    }


     if (track->GetCurrentStepNumber() > 1000) 
    {
        track->SetTrackStatus(fStopAndKill);
    }
}
