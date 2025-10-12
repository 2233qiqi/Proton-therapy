#include <iostream>
#include <fstream>
#include <string>

#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "G4UIExecutive.hh"
#include "G4VisManager.hh"
#include "G4VisExecutive.hh"
#include "G4NuclideTable.hh"

#include "DetectorConstruction.hh"
#include "ActionInitialization.hh"
#include "PhysicsList.hh"

int main(int argc, char **argv)
{
    
    std::ofstream logfile("run.log");
    G4cout.rdbuf(logfile.rdbuf());
    
    G4UIExecutive *ui = nullptr;
    if (argc == 1)
    {
        ui = new G4UIExecutive(argc, argv);
    }

    auto *runManager = new G4RunManager;

    runManager->SetUserInitialization(new PhysicsList());
    runManager->SetUserInitialization(new DetectorConstruction());
    runManager->SetUserInitialization(new ActionInitialization());

    runManager->Initialize();

    G4VisManager *visManager = new G4VisExecutive("Quiet");
    visManager->Initialize();

    G4UImanager *uiManager = G4UImanager::GetUIpointer();
   
    if(argc == 4)
    {
        int particle_count=std::stoi(argv[1]);
        std::string particle_type = argv[2];
        std::string particle_direction = argv[3];
        
        std::cout << "Running in batch mode with " << particle_count 
        <<"  and particle_type  "<<particle_type
        <<"  and particle_direction  "<<particle_direction
        <<std::endl;
     //设置粒子类别
       G4String particleCmd = "/gps/particle " + particle_type;
       uiManager->ApplyCommand(particleCmd);
     //判断粒子方向
       if (particle_direction == "iso")
       {
 
        uiManager->ApplyCommand("/gps/ang/type iso");
   
       }
       else
       {
        G4String directionCmd = "/gps/direction " + particle_direction;
        uiManager->ApplyCommand(directionCmd);
    
        uiManager->ApplyCommand("/gps/ang/type direction");
       }
     //运行对应的宏文件
        uiManager->ApplyCommand("/control/execute run_particle.mac"); 

         G4String beamCmd = "/run/beamOn " + std::to_string(particle_count);
            uiManager->ApplyCommand(beamCmd);
    }

    else
    {
        std::cerr << "\nERROR: Incorrect number of arguments. Expected 3, got " << argc - 1 << ".\n";
        std::cerr << "Usage: ./exampleB1  <N_events> <ParticleType> \"<Dir X Y Z>\"\n";
        std::cerr << "Example: ./exampleB1 10000 gamma \"0 0 1\"\n" << std::endl;
        
    }

    delete visManager;
    delete runManager;

    return 0;
}
