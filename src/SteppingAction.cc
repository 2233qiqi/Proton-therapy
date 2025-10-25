#include "SteppingAction.hh"
#include "EventAction.hh"
#include "G4Step.hh"
#include "G4LogicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include <cmath>

std::vector<G4double> SteppingAction::fDepthEdep;  
G4int SteppingAction::fNBins = 100;                 
G4double SteppingAction::fMaxDepth = 10.0 * CLHEP::mm;  

SteppingAction::SteppingAction(EventAction* eventAction)
    : fEventAction(eventAction)
{

    fDepthEdep.assign(fNBins, 0.0);
}

SteppingAction::~SteppingAction() = default;


void SteppingAction::UserSteppingAction(const G4Step* step)
{
    G4LogicalVolume* volume = step->GetPreStepPoint()->GetPhysicalVolume()->GetLogicalVolume();
    G4double edep = step->GetTotalEnergyDeposit();

    if (edep <= 0.) return;

    if (volume->GetName() == "Detector") {
        fEventAction->AddEnergyDeposit(edep);
    }

    if (volume->GetName() == "Shield") {
        G4double z = step->GetPreStepPoint()->GetPosition().z();
        G4double shieldFrontZ = -5. * mm - fMaxDepth / 2.0;
        G4double shieldBackZ = shieldFrontZ + fMaxDepth;

        if (z >= shieldBackZ) {  
            G4LogicalVolume* nextVolume = step->GetPostStepPoint()->GetPhysicalVolume()->GetLogicalVolume();
            if (nextVolume && nextVolume->GetName() == "Detector") {
                fEventAction->AddEnergyDeposit(edep);  
            }
        }
    }
}

