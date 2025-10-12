#include "DetectorConstruction.hh"
#include "G4Color.hh"
#include "G4VisAttributes.hh"
#include "G4PVReplica.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"




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

  G4Box *solidWorld =new G4Box ("World",10*cm ,10*cm ,10*cm);
  G4LogicalVolume *





}