#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4UIExecutive.hh"
#include "G4SteppingVerbose.hh"
#include "G4VisExecutive.hh"

#include "DetectorConstruction.hh"
#include "PhysicsList.hh"
#include "PrimaryGenerator.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

#include <string>

bool isMacroFile(const char* filename)
{
    std::string str(filename);
    return str.size() >= 4 && str.substr(str.size()-4) == ".mac";
}

int main(int argc, char **argv)
{
    G4UIExecutive* ui = nullptr;
    if (argc == 1) {
        ui = new G4UIExecutive(argc, argv);
    }

    G4SteppingVerbose::UseBestUnit(4);

    auto runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Serial);

    auto detConstruction = new DetectorConstruction();
    runManager->SetUserInitialization(detConstruction);

    auto physicsList = new PhysicsList();
    physicsList->SetVerboseLevel(1);
    runManager->SetUserInitialization(physicsList);

    runManager->SetUserAction(new PrimaryGeneratorAction);

    auto runAction = new RunAction(detConstruction); 
    auto eventAction = new EventAction(runAction);  
    auto steppingAction = new SteppingAction(eventAction); 

    runManager->SetUserAction(runAction);
    runManager->SetUserAction(eventAction);
    runManager->SetUserAction(steppingAction);

    runManager->Initialize();

    auto visManager = new G4VisExecutive("Quiet");
    visManager->Initialize();

    auto UImanager = G4UImanager::GetUIpointer();

    if (argc > 1)
    {
        G4String command = "/control/execute " + G4String(argv[1]);
        UImanager->ApplyCommand(command);
     
        delete visManager;
        delete runManager;
        return 0;
    }
    else 
    {
        
        UImanager->ApplyCommand("/control/execute vis.mac");
        UImanager->ApplyCommand("/control/execute run.mac");

        if (ui) {
            ui->SessionStart();
            delete ui;
        }
    }
    
    delete visManager;
    delete runManager;
    return 0;
}