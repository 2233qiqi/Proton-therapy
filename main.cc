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

int main(int argc, char **argv)
{
    G4UIExecutive* ui = nullptr;
    if (argc == 1) {
        ui = new G4UIExecutive(argc, argv);
    }

    G4int precision = 4;
    G4SteppingVerbose::UseBestUnit(precision);

    // Create run manager (serial mode)
    auto runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Serial); // 明确指定 Serial

    // Detector
    auto detConstruction = new DetectorConstruction();
    runManager->SetUserInitialization(detConstruction);

    // Physics
    auto physicsList = new PhysicsList();
    physicsList->SetVerboseLevel(1);
    runManager->SetUserInitialization(physicsList);

    runManager->SetUserAction(new PrimaryGeneratorAction);

    auto runAction = new RunAction();
    auto eventAction = new EventAction(runAction);
    auto steppingAction = new SteppingAction(eventAction);

    runManager->SetUserAction(runAction);
    runManager->SetUserAction(eventAction);
    runManager->SetUserAction(steppingAction);

    // Initialize kernel
    runManager->Initialize();

    // Visualization
    auto visManager = new G4VisExecutive("Quiet");
    visManager->Initialize();

    // UI
    auto UImanager = G4UImanager::GetUIpointer();
    if (!ui) {
        G4String command = "/control/execute ";
        G4String fileName = argv[1];
        UImanager->ApplyCommand(command + fileName);
    } else {
        UImanager->ApplyCommand("/control/execute vis.mac");
        ui->SessionStart();
        delete ui;
    }

    delete visManager;
    delete runManager;

    return 0;
}