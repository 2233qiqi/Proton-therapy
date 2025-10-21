#include "PhysicsList.hh"

#include "G4EmStandardPhysics_option4.hh"      
#include "G4EmExtraPhysics.hh"               
#include "G4DecayPhysics.hh"
#include "G4RadioactiveDecayPhysics.hh"


#include "G4HadronElasticPhysicsHP.hh"         
#include "G4HadronPhysicsQGSP_BIC_HP.hh"       
#include "G4StoppingPhysics.hh"
#include "G4IonPhysics.hh"
#include "G4NeutronTrackingCut.hh"

PhysicsList::PhysicsList()
{
    
    RegisterPhysics(new G4EmStandardPhysics_option4());

    RegisterPhysics(new G4EmExtraPhysics());

    RegisterPhysics(new G4DecayPhysics());
    RegisterPhysics(new G4RadioactiveDecayPhysics());

    RegisterPhysics(new G4HadronElasticPhysicsHP());
    RegisterPhysics(new G4HadronPhysicsQGSP_BIC_HP());

    RegisterPhysics(new G4StoppingPhysics());

    RegisterPhysics(new G4IonPhysics());

    RegisterPhysics(new G4NeutronTrackingCut());
}

PhysicsList::~PhysicsList() 
{
    
}