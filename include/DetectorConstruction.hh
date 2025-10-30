#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"

class G4VPhysicalVolume;
class G4LogicalVolume;
class CommandMessenger;  

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    DetectorConstruction();
    ~DetectorConstruction() override;

    G4VPhysicalVolume* Construct() override;

    void SetShieldMaterial(const G4String& materialName);
    void SetShieldThickness(G4double thickness);
    void CalculateMass(); 
    G4double GetDetectorMass() const { return fDetectorMass; }

private:
    G4String fShieldMaterialName;
    G4double fShieldThickness;
    G4double fDetectorMass;

};

#endif
