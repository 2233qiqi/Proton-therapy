#include "EventAction.hh"
#include "RunAction.hh" 

EventAction::EventAction(RunAction* runAction)
    : fRunAction(runAction), fEnergyDeposit(0.)
{}

EventAction::~EventAction() = default;

void EventAction::BeginOfEventAction(const G4Event*)
{
    fEnergyDeposit = 0.; 
}

void EventAction::EndOfEventAction(const G4Event*)
{

    if (fEnergyDeposit > 0.0) {

        fRunAction->AddTotalEnergyAndCount(fEnergyDeposit); 
    }
}

