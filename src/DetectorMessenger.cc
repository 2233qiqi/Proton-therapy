#include "DetectorMessenger.hh"
#include "DetectorConstruction.hh"

#include "G4UIcmdWithAString.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4SystemOfUnits.hh" 

DetectorMessenger::DetectorMessenger(DetectorConstruction* det)
    : G4UImessenger(), fDetectorConstruction(det)
{

    fMatCmd = new G4UIcmdWithAString("/shield/material", this);
    fMatCmd->SetGuidance("Select shield material (e.g., G4_Pb).");
    fMatCmd->SetParameterName("materialName", false);
    fMatCmd->AvailableForStates(G4State_PreInit, G4State_Idle); 

    fThickCmd = new G4UIcmdWithADoubleAndUnit("/shield/thickness", this);
    fThickCmd->SetGuidance("Set shield thickness (e.g., 5.0 cm).");
    fThickCmd->SetParameterName("thickness", false);
    fThickCmd->SetDefaultUnit("cm");
    fThickCmd->AvailableForStates(G4State_PreInit, G4State_Idle);
}

DetectorMessenger::~DetectorMessenger()
{
    delete fMatCmd;
    delete fThickCmd;
}

void DetectorMessenger::SetNewValue(G4UIcommand* command, G4String newValues)
{
    if (command == fMatCmd)
    {
        fDetectorConstruction->SetShieldMaterial(newValues);
    }
    else if (command == fThickCmd)
    {
        G4double thickness = fThickCmd->GetNewDoubleValue(newValues);
        fDetectorConstruction->SetShieldThickness(thickness);
    }
}