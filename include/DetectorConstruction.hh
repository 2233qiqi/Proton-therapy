#ifndef DETECTORCONSTRUCTION_HH
#define DETECTORCONSTRUCTION_HH

#include "G4VUserDetectorConstruction.hh"
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    DetectorConstruction();
    virtual ~DetectorConstruction();

    virtual G4VPhysicalVolume* Construct();
  
    G4LogicalVolume* GetPhantomLogicalVolume() const { return fLogicalModle; }
    G4double GetPhantomSizeX() const { return fModleSizeX; }
    G4double GetPhantomSizeY() const { return fModleSizeY; }
    G4double GetPhantomSizeZ() const { return fModleSizeZ; }
    G4int GetNumberOfVoxelsZ() const { return fNVoxelsZ; }

protected:
   
    virtual void ConstructSDandField();

private:

    G4double fModleSizeX = 8.0 * cm;
    G4double fModleSizeY = 8.0 * cm;
    G4double fModleSizeZ = 16.0 * cm; 
    G4int fNVoxelsZ = 320; 
    G4double fWorldSizeZ = 20.0 * cm;


    G4LogicalVolume* fLogicalModle;
    G4NistManager* fNistManager;
};

#endif
