#ifndef G4DoseActionInitialization_h
#define G4DoseActionInitialization_h 1

#include "G4VUserActionInitialization.hh"

// 前向声明，以避免循环引用和冗余头文件
class G4DoseDetectorConstruction; 

class G4DoseActionInitialization : public G4VUserActionInitialization
{
public:
    // 构造函数：需要接收 DetectorConstruction 指针，以便传递给其他 Action
    G4DoseActionInitialization(G4DoseDetectorConstruction* det);
    ~G4DoseActionInitialization() override = default;

    // 必须实现的虚函数
    void Build() const override;
    void BuildForMaster() const override;

private:
    // 存储 DetectorConstruction 的指针，用于传递给其他 Action
    G4DoseDetectorConstruction* fDetConstruction;
    
    // 关键方法：用于在 Build() 中定义和设置剂量采集器 (MFD)
    void DefineScorers() const;
};

#endif
