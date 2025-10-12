#include "DetectorConstruction.hh"
#include "G4Color.hh"
#include "G4VisAttributes.hh"
#include "G4PVReplica.hh"
#include "G4NistManager.hh"

DetectorConstruction::DetectorConstruction()
{

};
DetectorConstruction :: ~DetectorConstruction()
{

}


G4VPhysicalVolume * DetectorConstruction :: Construct()
{
  G4bool checkOverlaps = true;

  fNistManager->FindOrBuildMaterial("G4_AIR");
  fNistManager->FindOrBuildMaterial("G4_Water");
  G4Material *worldMaterial = fNistManager->FindOrBuildMaterial("G4_AIR");
  





}