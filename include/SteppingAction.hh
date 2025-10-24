#ifndef SteppingAction_h
#define SteppingAction_h 1

#include "G4UserSteppingAction.hh"

class EventAction;

class SteppingAction : public G4UserSteppingAction
{
public:
    SteppingAction(EventAction* eventAction);
    ~SteppingAction() override;

    void UserSteppingAction(const G4Step* step) override;
    void AddShieldEdep(G4double depth, G4double edep);

private:
    EventAction* fEventAction;
    static std::vector<G4double> fDepthEdep;   
    static G4int fNBins;
    static G4double fMaxDepth; 
};

#endif