#ifndef SteppingAction_h
#define SteppingAction_h 1

#include "G4UserSteppingAction.hh"
#include "globals.hh"
#include <vector>

class EventAction;

class SteppingAction : public G4UserSteppingAction
{
public:
    SteppingAction(EventAction* eventAction);
    ~SteppingAction() override;

    void UserSteppingAction(const G4Step* step) override;
    void AddShieldEdep(G4double depth, G4double edep);

    static const std::vector<G4double>& GetDepthEdep() { return fDepthEdep; }
    static G4int GetNBins() { return fNBins; }
    static G4double GetMaxDepth() { return fMaxDepth; }

private:
    EventAction* fEventAction;

    static std::vector<G4double> fDepthEdep;
    static G4int fNBins;
    static G4double fMaxDepth;
};

#endif
