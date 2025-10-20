#include "DetectorConstruction.hh"

#include "G4Box.hh"
#include "G4Cons.hh"
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4Trd.hh"

G4VPhysicalVolume *DetectorConstruction::Construct()
{
  G4NistManager* nist = G4NistManager::Instance();
  G4double shield_sizeXY = 50 * cm, shield_sizeZ = 50 * cm;
 
  G4bool checkOverlaps = true;

 //世界
  G4double world_sizeXY = 1.2 * shield_sizeXY;
  G4double world_sizeZ = 1.2 * shield_sizeZ;
  G4Material* world_mat = nist->FindOrBuildMaterial("G4_AIR");

  auto solidWorld =
    new G4Box("World",  
              0.5 * world_sizeXY, 0.5 * world_sizeXY, 0.5 * world_sizeZ); 

  auto logicWorld = new G4LogicalVolume(solidWorld,  
                                        world_mat,  
                                        "World");  

  auto physWorld = new G4PVPlacement(NULL, 
                                     G4ThreeVector(),  
                                     logicWorld,  
                                     "World",  
                                     NULL,  
                                     false, 
                                     0,  
                                     checkOverlaps);  

  //屏蔽材料
  G4Material* shield_mat = nist->FindOrBuildMaterial("G4_Pb");

  auto solidShield = new G4Box("Shield",0.5*shield_sizeXY,0.5 * shield_sizeXY,0.5*shield_sizeZ);
  
  auto logicaShield = new G4LogicalVolume(solidShield,shield_mat,"Shield");

  auto physShield =new G4PVPlacement(NULL,G4ThreeVector(),logicaShield,"Shield",logicWorld,false,0,checkOverlaps);

     return physWorld;
}