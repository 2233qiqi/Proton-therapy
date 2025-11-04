#include "PrimaryGenerator.hh"
#include "G4ParticleGun.hh"
#include "G4Event.hh"
#include "G4ParticleTable.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction()
{
    fParticleGun = new G4ParticleGun(1); 
    fParticleGun->SetParticleEnergy(1.0 * MeV); 
}

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
    delete fParticleGun;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* event)
{
   
    fParticleGun->GeneratePrimaryVertex(event);
}

void PrimaryGeneratorAction::SetEnergy(G4double energy_MeV)
{
    fParticleGun->SetParticleEnergy(energy_MeV * MeV);
}

void PrimaryGeneratorAction::SetParticle(G4String particleName)
{
    auto particleTable = G4ParticleTable::GetParticleTable();
    auto particle = particleTable->FindParticle(particleName);
    if (particle) {
        fParticleGun->SetParticleDefinition(particle);
    } else {
        G4cerr << "### Particle [" << particleName << "] not found!" << G4endl;
    }
}