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

    // ✅ 访问函数（供 RunAction 使用）
    static const std::vector<G4double>& GetDepthEdep() { return fDepthEdep; }
    static G4int GetNBins() { return fNBins; }
    static G4double GetMaxDepth() { return fMaxDepth; }

private:
    EventAction* fEventAction;

    // ✅ 静态成员：全体事件共享的深度沉积分布信息
    static std::vector<G4double> fDepthEdep;
    static G4int fNBins;
    static G4double fMaxDepth;
};

#endif
