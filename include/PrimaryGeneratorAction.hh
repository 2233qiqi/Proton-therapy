#ifndef PRIMARYGENERATOR_HH
#define PRIMARYGENERATOR_HH

#include "G4GeneralParticleSource.hh"
#include "G4ParticleDefinition.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4SystemOfUnits.hh"
#include "G4VUserPrimaryGeneratorAction.hh"

class PrimaryGenerator : public G4VUserPrimaryGeneratorAction
{
  public:
    PrimaryGenerator();
    virtual ~PrimaryGenerator();
    virtual void GeneratePrimaries(G4Event *);

  private:
    G4ParticleGun *fParticleGun;
    G4ParticleTable *particleTable;
    G4ParticleDefinition *particleDefinition;
    G4GeneralParticleSource *fGPS;

};



#endif