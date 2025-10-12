#include "PrimaryGeneratorAction.hh"

#include "G4GeneralParticleSource.hh"
#include "G4ParticleDefinition.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4SystemOfUnits.hh"
#include "G4VUserPrimaryGeneratorAction.hh"

PrimaryGenerator :: PrimaryGenerator() : G4VUserPrimaryGeneratorAction()
{
    fGPS->~G4GeneralParticleSource();
} 

void PrimaryGenerator::GeneratePrimaries(G4Event *event)
{
    fGPS->GeneratePrimaryVertex(event);
}
PrimaryGenerator::~PrimaryGenerator()
{
    delete fGPS;
}