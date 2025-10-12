#include "PhysicsList.hh"
#include "G4SystemOfUnits.hh"

#include "G4DecayPhysics.hh"
#include "G4EmStandardPhysics_option4.hh" 
#include "G4HadronPhysicsFTFP_BERT_HP.hh"

#include "G4ParticleDefinition.hh"
#include "G4Gamma.hh"
#include "G4Electron.hh"
#include "G4Positron.hh"


#include "G4ProductionCutsTable.hh"
#include "G4LossTableManager.hh"

PhysicsList :: PhysicsList() : G4VModularPhysicsList()
{
   SetVerboseLevel(1); 

   RegisterPhysics(new G4EmStandardPhysics_option4());//电磁物理

   RegisterPhysics(new G4HadronPhysicsFTFP_BERT_HP());//强子物理

   RegisterPhysics(new G4DecayPhysics());//粒子衰变物理

};

PhysicsList :: ~PhysicsList()
{

};

void PhysicsList :: SetCut()
{
   G4VUserPhysicsList::SetCuts();

   defaultCutValue = 1 *nm;
   
}