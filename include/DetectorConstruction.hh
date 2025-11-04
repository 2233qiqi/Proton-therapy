// DetectorConstruction.hh

#ifndef DetectorConstruction_hh
#define DetectorConstruction_hh 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"
#include "G4SystemOfUnits.hh"
#include "G4UImessenger.hh"        
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4UIcmdWithAString.hh"

class G4VPhysicalVolume;
class G4LogicalVolume;
class DetectorMessenger; 

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    DetectorConstruction();
    ~DetectorConstruction() override;

public:
    G4VPhysicalVolume* Construct() override;
    void ConstructSDandField() override; 
    
    void SetShieldMaterial(const G4String& materialName);
    void SetShieldThickness(G4double thickness);

    G4double GetDetectorMass() const { return fDetectorMass; }

private:
    G4String fShieldMaterialName;
    G4double fShieldThickness;
    G4double fDetectorMass = 0.0; 
    
    DetectorMessenger* fDetectorMessenger; 
};

#endif