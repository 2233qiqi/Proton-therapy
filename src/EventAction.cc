#include "EventAction.hh"

#include "G4AnalysisManager.hh"
#include "G4Event.hh"
#include "G4TrajectoryContainer.hh"
#include "G4ios.hh"
#include "G4SDManager.hh"

EventAction::EventAction(const RunAction *run) {}

void EventAction::BeginOfEventAction(const G4Event *) {}

void EventAction::EndOfEventAction(const G4Event *event)
{

}