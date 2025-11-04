// DetectorMessenger.hh

#ifndef DetectorMessenger_hh
#define DetectorMessenger_hh 1

#include "G4UImessenger.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4UIcmdWithAString.hh"
#include "globals.hh"

class DetectorConstruction; 

class DetectorMessenger : public G4UImessenger
{
public:
    DetectorMessenger(DetectorConstruction* det);
    ~DetectorMessenger() override;

    void SetNewValue(G4UIcommand* command, G4String newValues) override;

private:
    DetectorConstruction* fDetectorConstruction;
    
    G4UIcmdWithAString* fMatCmd;
    G4UIcmdWithADoubleAndUnit* fThickCmd;
};

#endif