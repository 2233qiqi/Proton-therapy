#ifndef PhysicsList_h
#define PhysicsList_h

#include  "G4VModularPhysicsList.hh"

class PhysicsList : public G4VModularPhysicsList
{
    public:
    PhysicsList();
    virtual ~PhysicsList();
  
    virtual void SetCut();

};


#endif