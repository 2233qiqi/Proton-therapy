#ifndef B2EventAction_h
#define B2EventAction_h

#include "G4UserEventAction.hh"
#include "RunAction.hh"

class G4Event;

class EventAction : public G4UserEventAction
{
public:
  EventAction(const RunAction *run);
  ~EventAction() override = default;

  void BeginOfEventAction(const G4Event *) override;
  void EndOfEventAction(const G4Event *) override;
};

#endif