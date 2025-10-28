#ifndef CommandMessenger_h
#define CommandMessenger_h 1

#include "G4UImessenger.hh"
#include "G4UIcmdWithAString.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "globals.hh"

class DetectorConstruction;

class CommandMessenger : public G4UImessenger {
public:
    CommandMessenger(DetectorConstruction* detector);
    ~CommandMessenger() override;

    void SetNewValue(G4UIcommand* command, G4String newValue) override;

private:
    DetectorConstruction* fDetector = nullptr;

    G4UIdirectory* fCommandDir = nullptr;
    G4UIcmdWithAString* fShieldMatCmd = nullptr;
    G4UIcmdWithADoubleAndUnit* fShieldThickCmd = nullptr;
};

#endif
