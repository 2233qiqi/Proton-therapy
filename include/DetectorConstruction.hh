#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"

class G4VPhysicalVolume;
class G4LogicalVolume;

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    DetectorConstruction();
    ~DetectorConstruction() override;

    G4VPhysicalVolume* Construct() override;

    void SetShieldMaterial(const G4String& materialName);
    void SetShieldThickness(G4double thickness); 

private:
    G4LogicalVolume* fDetectorLogic; 

    G4String fShieldMaterialName;
    G4double fShieldThickness;
};

#endif