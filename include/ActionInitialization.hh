#ifndef ACTIONINITIALIZATION_HH
#define ACTIONINITIALIZATION_HH
#include "G4VUserActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"

class ActionInitialization : public G4VUserActionInitialization
{
public:
    ActionInitialization() = default;
    ~ActionInitialization() override = default;

    // Method to build user actions
    void Build() const override;

    // Method to build user actions for the master thread
    void BuildForMaster() const override;
};

#endif