#include "DetectorConstruction.hh"

#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"
#include "G4VisAttributes.hh"

DetectorConstruction::DetectorConstruction()
    : 
      fShieldMaterialName("G4_Pb"),
      fShieldThickness(5.0 * cm)
{}

DetectorConstruction::~DetectorConstruction() = default;

G4VPhysicalVolume* DetectorConstruction::Construct()
{
    G4NistManager* nist = G4NistManager::Instance();
    G4bool checkOverlaps = true;

    // world
    G4double worldSize = 2.0 * m;
    G4Material *worldmat = nist ->FindOrBuildMaterial("G4_AIR");

    auto solidWorld = new G4Box("World", worldSize/2, worldSize/2, worldSize/2);
    auto logicWorld = new G4LogicalVolume(solidWorld, worldmat, "World");
    auto physWorld = new G4PVPlacement(nullptr, G4ThreeVector(), logicWorld, "World", nullptr, false, 0, checkOverlaps);
    
    G4VisAttributes *worldVisAtt = new G4VisAttributes(G4Colour(0.0, 0.0, 0.0, 0.3));
    worldVisAtt->SetVisibility(false);
    logicWorld->SetVisAttributes(worldVisAtt);
    // shield
    G4double shieldX = 30. * cm;   
    G4double shieldY = 30. * cm;
    G4double shieldZ = fShieldThickness;
    G4Material* shieldMat = nist->FindOrBuildMaterial(fShieldMaterialName);

    auto solidShield = new G4Box("Shield", shieldX/2, shieldY/2, shieldZ/2);
    auto logicalSheild = new G4LogicalVolume(solidShield, shieldMat, "Shield");
    auto physsheild = new G4PVPlacement(nullptr,
                      G4ThreeVector(0, 0,0),
                      logicalSheild,
                      "Shield",
                      logicWorld,
                      false,
                      0,
                      checkOverlaps);

    G4VisAttributes* shieldVis = new G4VisAttributes(G4Colour(0.3, 0.3, 0.8)); 
    shieldVis->SetLineWidth(2);
    logicalSheild->SetVisAttributes(shieldVis);

    // Detector 
    G4double detZ = 1.0 * mm; 
    G4double detPosZ = shieldZ/2 + detZ/2 + 0.1 * mm; 
    G4Material* detMat = nist->FindOrBuildMaterial("G4_WATER"); 

    auto solidDet = new G4Box("Detector", shieldX/2, shieldY/2, detZ/2);
    auto logicalDet = new G4LogicalVolume(solidDet,detMat,"Detector");
    auto physDet = new G4PVPlacement(nullptr,
                      G4ThreeVector(0, 0, detPosZ),
                      logicalDet,
                      "Detector",
                      logicWorld,
                      false,
                      0,
                      checkOverlaps);

    G4VisAttributes* detVis = new G4VisAttributes(G4Colour(1.0, 0., 0.0, 0.8)); 
    detVis->SetLineWidth(2);
    logicalDet->SetVisAttributes(detVis);

    return physWorld;

    return physWorld;
}

// commands
void DetectorConstruction::SetShieldMaterial(const G4String& materialName)
{
    fShieldMaterialName = materialName;
}

void DetectorConstruction::SetShieldThickness(G4double thickness)
{
    fShieldThickness = thickness;
}