#include "ActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"


#include "G4UserRunAction.hh"
#include "G4UserEventAction.hh"
#include "G4UserSteppingAction.hh"

#include "G4MultiFunctionalDetector.hh"
#include "G4VPrimitiveScorer.hh"
#include "G4PSEnergyDeposit.hh"
#include "G4SDManager.hh"
#include "DetectorConstruction.hh"
#include "G4LogicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include "G4ios.hh"


ActionInitialization::ActionInitialization(DetectorConstruction* det)
: G4VUserActionInitialization(),
  fDetConstruction(det)
{
    DefineScorers();
}

//....oooOOO0OOooo........oooOOO0OOooo........oooOOO0OOooo........oooOOO0OOooo......

void ActionInitialization::DefineScorers() const
{
    G4String detectorName = "PhantomSD";
    G4MultiFunctionalDetector* phantomSD = new G4MultiFunctionalDetector(detectorName);
    
    G4String primitiveName = "DoseDeposit";
    G4VPrimitiveScorer* scorer = new G4PSEnergyDeposit(primitiveName);
    
    phantomSD->RegisterPrimitive(scorer);
    
    G4SDManager* sdm = G4SDManager::GetSDMpointer();
    sdm->AddNewDetector(phantomSD);

    G4LogicalVolume* phantomLV = fDetConstruction->GetPhantomLogicalVolume(); 
    
    if (phantomLV) {
        phantomLV->SetSensitiveDetector(phantomSD);

        G4int nZCells = fDetConstruction->GetNumberOfVoxelsZ();
        
        G4cout << "Configuring Scoring Mesh for " << phantomLV->GetName() 
               << " with " << nZCells << " voxels along Z." << G4endl;
        
    } else {
        G4cerr << "ERROR: Phantom Logical Volume not found for Scorer attachment!" << G4endl;
    }
}



void ActionInitialization::BuildForMaster() const
{
    // G4VUserRunAction 现在已被定义
    G4UserRunAction* runAction = new RunAction(fDetConstruction, nullptr);
    SetUserAction(runAction);
}


void ActionInitialization::Build() const
{
    // PrimaryGeneratorAction (调用需要匹配 PrimaryGeneratorAction.hh 的新签名)
    SetUserAction(new PrimaryGeneratorAction(fDetConstruction)); 

    
    G4UserRunAction* runAction = new RunAction(fDetConstruction, nullptr);
    SetUserAction(runAction);

    // G4VUserEventAction 现在已被定义
    // EventAction (调用需要匹配 EventAction.hh 的新签名)
    G4UserEventAction* eventAction = new EventAction();
    SetUserAction(eventAction);

    // G4VUserSteppingAction 现在已被定义
    SetUserAction(new SteppingAction());
}
