#ifndef ActionInitialization_h
#define ActionInitialization_h 1

#include "G4VUserActionInitialization.hh"


class DetectorConstruction; 

class ActionInitialization : public G4VUserActionInitialization
{
public:

    ActionInitialization(DetectorConstruction* det);
    ~ActionInitialization() override = default;
    void Build() const override;
    void BuildForMaster() const override;

private:
    DetectorConstruction* fDetConstruction;
    
    void DefineScorers() const;
};

#endif
