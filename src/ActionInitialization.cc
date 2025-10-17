#include "ActionInitialization.hh"
#include "RunAction.hh"
#include "EventAction.hh"

void ActionInitialization::BuildForMaster() const
{

  //SetUserAction(new PrimaryGeneratorAction());
  //auto runAction = new RunAction;
  SetUserAction(new RunAction);
  //auto eventAction = new EventAction(runAction);
  //SetUserAction(eventAction);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void ActionInitialization::Build() const
{
  SetUserAction(new PrimaryGeneratorAction());

  auto runAction = new RunAction;
  SetUserAction(runAction);

  auto eventAction = new EventAction(runAction);
  SetUserAction(eventAction);

  // SetUserAction(new SteppingAction(eventAction));
}
