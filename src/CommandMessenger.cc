#include "CommandMessenger.hh"
#include "DetectorConstruction.hh"
#include "G4UIdirectory.hh"
#include "G4SystemOfUnits.hh"

CommandMessenger::CommandMessenger(DetectorConstruction* detector)
: fDetector(detector)
{
    fCommandDir = new G4UIdirectory("/command/");
    fCommandDir->SetGuidance("User commands for geometry control.");

    fShieldMatCmd = new G4UIcmdWithAString("/command/setShieldMaterial", this);
    fShieldMatCmd->SetGuidance("Set shield material (e.g. G4_Pb, G4_Al, G4_Cu).");

    fShieldThickCmd = new G4UIcmdWithADoubleAndUnit("/command/setShieldThickness", this);
    fShieldThickCmd->SetGuidance("Set shield thickness.");
    fShieldThickCmd->SetUnitCategory("Length");
}

CommandMessenger::~CommandMessenger()
{
    delete fShieldMatCmd;
    delete fShieldThickCmd;
    delete fCommandDir;
}

void CommandMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{
    if (command == fShieldMatCmd) {
        fDetector->SetShieldMaterial(newValue);
    } else if (command == fShieldThickCmd) {
        fDetector->SetShieldThickness(fShieldThickCmd->GetNewDoubleValue(newValue));
    }
}
