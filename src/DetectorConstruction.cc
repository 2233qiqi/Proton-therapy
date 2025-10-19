#include "DetectorConstruction.hh"
#include "G4Color.hh"
#include "G4VisAttributes.hh"
#include "G4PVReplica.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4GeometryManager.hh"

DetectorConstruction::DetectorConstruction()
: fNistManager(G4NistManager::Instance())
{
}

DetectorConstruction::~DetectorConstruction()
{
}

G4VPhysicalVolume* DetectorConstruction::Construct()
{
    G4GeometryManager::GetInstance()->OpenGeometry();
    G4GeometryManager::GetInstance()->SetWorldMaximumExtent(fWorldSizeZ);

    G4bool checkOverlaps = true;

    G4Material* worldMaterial = fNistManager->FindOrBuildMaterial("G4_AIR");
    G4Material* modleMaterial = fNistManager->FindOrBuildMaterial("G4_WATER");

    G4Box* solidWorld = new G4Box("World", fModleSizeX/2.0 + 1.0*cm, fModleSizeY/2.0 + 1.0*cm, fWorldSizeZ/2.0);
    G4LogicalVolume* logicalWorld = new G4LogicalVolume(solidWorld, worldMaterial, "World");
    G4VPhysicalVolume* physWorld = new G4PVPlacement(0, G4ThreeVector(0,0,0), logicalWorld, "World", 0, false, 0, checkOverlaps);

    G4Box* solidModle = new G4Box("Modle", fModleSizeX/2.0, fModleSizeY/2.0, fModleSizeZ/2.0);
    fLogicalModle = new G4LogicalVolume(solidModle, modleMaterial, "ModleLV");

    G4double Z_position = fModleSizeZ / 2.0;
    G4PVPlacement* physModle = new G4PVPlacement(0, G4ThreeVector(0, 0, Z_position), fLogicalModle, "PhysModle", logicalWorld, false, 0, checkOverlaps);

    G4double voxel_dz = fModleSizeZ / fNVoxelsZ;
    G4Box* solidVoxel = new G4Box("Voxel", fModleSizeX/2.0, fModleSizeY/2.0, voxel_dz/2.0);
    G4LogicalVolume* logicalVoxel = new G4LogicalVolume(solidVoxel, modleMaterial, "VoxelLV");

    new G4PVReplica("VoxelReplica", logicalVoxel, fLogicalModle, kZAxis, fNVoxelsZ, voxel_dz, checkOverlaps);

    logicalWorld->SetVisAttributes(G4VisAttributes::GetInvisible());

    G4VisAttributes* modleVisAtt = new G4VisAttributes(G4Color(0.2, 0.8, 0.9, 0.5));
    modleVisAtt->SetForceSolid(true);
    fLogicalModle->SetVisAttributes(modleVisAtt);

    G4VisAttributes* voxelVisAtt = new G4VisAttributes(G4Color(G4Color::Yellow()));
    voxelVisAtt->SetForceWireframe(true);
    logicalVoxel->SetVisAttributes(voxelVisAtt);

    return physWorld;
}

void DetectorConstruction::ConstructSDandField()
{
}
