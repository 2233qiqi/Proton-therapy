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

    // Run manager
    auto runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Serial);

    // Detector and Physics
    auto detConstruction = new DetectorConstruction();
    runManager->SetUserInitialization(detConstruction);

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

    runManager->Initialize();

    // Visualization manager (Quiet mode)
    auto visManager = new G4VisExecutive("Quiet");
    visManager->Initialize();

    auto UImanager = G4UImanager::GetUIpointer();

    // -------------- 命令行模式 ----------------
    if (argc > 1)
    {
        if (isMacroFile(argv[1])) {
            // 执行宏文件
            UImanager->ApplyCommand("/control/execute " + G4String(argv[1]));
        } else {
            // 执行所有命令行命令（修改几何等）
            for (int i = 1; i < argc; i++)
                UImanager->ApplyCommand(argv[i]);

            // 自动重初始化几何
            UImanager->ApplyCommand("/run/reinitializeGeometry");

            G4cout << "Geometry updated according to command line inputs." << G4endl;
            G4cout << "Now run your macro file to perform the simulation." << G4endl;
        }

        delete visManager;
        delete runManager;
        return 0;
    }

    // -------------- 交互式 UI 模式 ----------------
    UImanager->ApplyCommand("/control/execute vis.mac");
    ui->SessionStart();
    delete ui;

    delete visManager;
    delete runManager;
    return 0;
}
