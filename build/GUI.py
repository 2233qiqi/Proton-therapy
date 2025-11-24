import sys
import subprocess
import os
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
                             QGroupBox, QTextEdit, QFileDialog, QMessageBox,
                             QProgressBar, QSplitter, QTabWidget, QFrame)
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

class SimulationThread(QThread):
    """
    后台模拟线程 (逻辑保持不变)
    """
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)
    progress_signal = pyqtSignal(int)

    def __init__(self, command, args):
        super().__init__()
        self.command = command
        self.args = args
        self.is_running = True

    def run(self):
        try:
            # 模拟业务逻辑
            self.output_signal.emit(f"System Info: Initializing run sequence...")
            self.output_signal.emit(f"Command: {self.command} {' '.join(self.args)}")
            self.output_signal.emit("-" * 50)
            
            for i in range(1, 101):
                if not self.is_running: 
                    self.output_signal.emit("Warning: Process aborted by user.")
                    break
                
                time.sleep(0.05) # 模拟耗时
                
                # 模拟一些专业的日志输出
                if i % 5 == 0:
                    self.output_signal.emit(f"[INFO] Event {i:04d}: Energy deposition calculation completed. delta_E=2.34 MeV")
                
                if i % 20 == 0:
                    self.output_signal.emit(f"[STATUS] Checkpoint reached: {i}% processing complete.")
                
                self.progress_signal.emit(i)

            if self.is_running:
                self.finished_signal.emit(0)

        except Exception as e:
            self.output_signal.emit(f"[ERROR] Exception: {str(e)}")
            self.finished_signal.emit(-1)

    def stop(self):
        self.is_running = False

class Geant4EnterpriseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulation_thread = None
        self.init_ui()

    def init_ui(self):
        # 全局字体设置 - 使用标准商用字体
        font = QFont("Segoe UI", 9)
        QApplication.setFont(font)

        self.setWindowTitle("Geant4 Simulation Platform - Enterprise Edition")
        self.resize(1024, 768)
        
        # 应用企业级白色主题
        self.apply_enterprise_theme()

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- 1. 顶部工具栏/标题栏区域 ---
        header_frame = QFrame()
        header_frame.setObjectName("HeaderFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        title_label = QLabel("Geant4 辐射屏蔽分析系统")
        title_label.setObjectName("AppTitle")
        
        version_label = QLabel("v2.4.0 Release")
        version_label.setObjectName("VersionLabel")

        self.status_label = QLabel("● Ready")
        self.status_label.setObjectName("StatusReady")

        header_layout.addWidget(title_label)
        header_layout.addWidget(version_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        
        main_layout.addWidget(header_frame)

        # --- 2. 主内容区分割 (左侧配置，右侧日志) ---
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)

        # 左侧：配置面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 5, 0)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_basic_tab(), "基本参数配置")
        self.tab_widget.addTab(self.create_advanced_tab(), "高级物理选项")
        
        left_layout.addWidget(self.tab_widget)
        
        # 底部控制栏 (位于左侧面板下方)
        control_frame = QFrame()
        control_frame.setObjectName("ControlFrame")
        control_layout = QVBoxLayout(control_frame)
        control_layout.setContentsMargins(15, 15, 15, 15)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Processing... %p%")
        self.progress_bar.setValue(0)
        
        # 按钮组
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("开始模拟 (Run)")
        self.run_btn.setObjectName("PrimaryButton")
        self.run_btn.clicked.connect(self.run_simulation)
        
        self.stop_btn = QPushButton("停止 (Stop)")
        self.stop_btn.clicked.connect(self.stop_simulation)
        self.stop_btn.setEnabled(False)
        
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.stop_btn)
        
        control_layout.addWidget(QLabel("任务进度:"))
        control_layout.addWidget(self.progress_bar)
        control_layout.addSpacing(10)
        control_layout.addLayout(btn_layout)
        
        left_layout.addWidget(control_frame)

        # 右侧：日志输出
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 0, 0, 0)
        
        log_header = QLabel("系统运行日志 (Execution Log)")
        log_header.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("等待任务启动...")
        
        clear_log_btn = QPushButton("清空日志")
        clear_log_btn.setFixedWidth(80)
        clear_log_btn.clicked.connect(self.clear_output)
        
        log_tools_layout = QHBoxLayout()
        log_tools_layout.addWidget(log_header)
        log_tools_layout.addStretch()
        log_tools_layout.addWidget(clear_log_btn)

        right_layout.addLayout(log_tools_layout)
        right_layout.addWidget(self.output_text)

        # 添加到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600]) # 初始比例
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        main_layout.addWidget(splitter)

    def apply_enterprise_theme(self):
        """应用正式的企业级QSS样式表"""
        self.setStyleSheet("""
            /* 全局设置 */
            QMainWindow, QWidget {
                background-color: #f0f2f5; /* 浅灰背景 */
                color: #333333;
            }
            
            /* 顶部标题栏 */
            QFrame#HeaderFrame {
                background-color: #ffffff;
                border-bottom: 1px solid #dcdcdc;
            }
            QLabel#AppTitle {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
            }
            QLabel#VersionLabel {
                color: #666666;
                margin-left: 10px;
                padding-top: 4px;
                font-size: 11px;
            }
            
            /* 状态标签 */
            QLabel#StatusReady { color: #107c10; font-weight: bold; }
            QLabel#StatusRunning { color: #0078d7; font-weight: bold; }
            QLabel#StatusError { color: #d13438; font-weight: bold; }

            /* 选项卡 */
            QTabWidget::pane {
                border: 1px solid #d1d1d1;
                background: #ffffff;
                top: -1px;
            }
            QTabBar::tab {
                background: #e1e1e1;
                border: 1px solid #d1d1d1;
                padding: 8px 20px;
                margin-right: 2px;
                color: #555;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom-color: #ffffff; /* 与pane融合 */
                color: #0078d7; /* 选中时文字变蓝 */
                font-weight: bold;
            }
            
            /* 分组框 */
            QGroupBox {
                background-color: #ffffff;
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 20px; /* 为标题留出空间 */
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                color: #0078d7; /* 标题蓝色 */
            }

            /* 输入控件 */
            QLineEdit, QComboBox {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                background: #ffffff;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0078d7;
            }
            QLineEdit:read-only {
                background-color: #f3f3f3;
                color: #666;
            }
            
            /* 按钮通用 */
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 6px 15px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #999999;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
            }
            
            /* 主操作按钮 (蓝色) */
            QPushButton#PrimaryButton {
                background-color: #0078d7;
                color: white;
                border: 1px solid #005a9e;
                font-weight: bold;
            }
            QPushButton#PrimaryButton:hover {
                background-color: #1084d9;
            }
            QPushButton#PrimaryButton:pressed {
                background-color: #005a9e;
            }
            QPushButton#PrimaryButton:disabled {
                background-color: #f3f3f3;
                color: #aaa;
                border-color: #ddd;
            }

            /* 日志文本框 */
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
                color: #333;
            }
            
            /* 进度条 */
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 3px;
                text-align: center;
                background-color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
            }

            /* 分割器 */
            QSplitter::handle {
                background-color: #dcdcdc;
            }
        """)

    def create_form_row(self, label_text, widget, unit_text=None, btn=None):
        """创建标准表单行"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 5, 0, 5)
        
        label = QLabel(label_text)
        label.setFixedWidth(110) # 固定标签宽度，保持对齐
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("color: #444;") # 深灰色字体
        
        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addWidget(widget)
        
        if unit_text:
            if isinstance(unit_text, str):
                unit = QLabel(unit_text)
                unit.setStyleSheet("color: #666;")
                layout.addWidget(unit)
            else:
                layout.addWidget(unit_text)
        
        if btn:
            layout.addWidget(btn)
            
        return container

    def create_basic_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 文件配置组
        file_group = QGroupBox("文件路径设置 (File Configuration)")
        file_layout = QVBoxLayout(file_group)
        
        self.exec_file_edit = QLineEdit("./main")
        browse_exec_btn = QPushButton("浏览...")
        browse_exec_btn.clicked.connect(self.browse_exec_file)
        file_layout.addWidget(self.create_form_row("可执行程序:", self.exec_file_edit, btn=browse_exec_btn))

        self.macro_file_edit = QLineEdit("run.mac")
        browse_macro_btn = QPushButton("浏览...")
        browse_macro_btn.clicked.connect(self.browse_macro_file)
        file_layout.addWidget(self.create_form_row("宏文件:", self.macro_file_edit, btn=browse_macro_btn))
        
        layout.addWidget(file_group)

        # 粒子源组
        source_group = QGroupBox("粒子源参数 (Source Parameters)")
        source_layout = QVBoxLayout(source_group)
        
        self.particle_combo = QComboBox()
        self.particle_combo.addItems(["Gamma Ray", "Electron (e-)", "Positron (e+)", "Proton", "Neutron"])
        source_layout.addWidget(self.create_form_row("粒子类型:", self.particle_combo))

        self.energy_edit = QLineEdit("1.0")
        self.energy_unit_combo = QComboBox()
        self.energy_unit_combo.addItems(["MeV", "GeV", "keV"])
        self.energy_unit_combo.setFixedWidth(70)
        source_layout.addWidget(self.create_form_row("初始能量:", self.energy_edit, unit_text=self.energy_unit_combo))
        
        layout.addWidget(source_group)
        layout.addStretch()
        return widget

    def create_advanced_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 几何材料
        geo_group = QGroupBox("几何与材料 (Geometry & Materials)")
        geo_layout = QVBoxLayout(geo_group)
        
        self.material_combo = QComboBox()
        self.material_combo.addItems(["Lead (Pb)", "Iron (Fe)", "Concrete", "Water", "Polyethylene"])
        geo_layout.addWidget(self.create_form_row("屏蔽层材料:", self.material_combo))

        self.thickness_edit = QLineEdit("10.0")
        geo_layout.addWidget(self.create_form_row("屏蔽层厚度:", self.thickness_edit, unit_text="cm"))
        
        layout.addWidget(geo_group)

        # 运行控制
        run_group = QGroupBox("计算控制 (Computation)")
        run_layout = QVBoxLayout(run_group)
        
        self.events_edit = QLineEdit("10000")
        run_layout.addWidget(self.create_form_row("模拟事件数:", self.events_edit, unit_text="Events"))
        
        self.threads_combo = QComboBox()
        self.threads_combo.addItems(["1 (Single Thread)", "2", "4", "8", "Auto-detect"])
        run_layout.addWidget(self.create_form_row("线程数:", self.threads_combo))
        
        layout.addWidget(run_group)
        layout.addStretch()
        return widget

    # --- 逻辑部分 (与之前保持兼容) ---
    
    def browse_macro_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择宏文件", "", "Macro Files (*.mac);;All Files (*)")
        if path: self.macro_file_edit.setText(path)

    def browse_exec_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择程序", "", "Executable (*.exe *);;All Files (*)")
        if path: self.exec_file_edit.setText(path)

    def run_simulation(self):
        # 界面状态更新
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("● Running")
        self.status_label.setObjectName("StatusRunning")
        self.status_label.style().unpolish(self.status_label) # 刷新样式
        self.status_label.style().polish(self.status_label)
        self.output_text.clear()
        self.progress_bar.setValue(0)

        # 收集参数 (示例)
        cmd = self.exec_file_edit.text()
        args = [
            self.macro_file_edit.text(),
            self.particle_combo.currentText(),
            self.energy_edit.text()
        ]

        self.simulation_thread = SimulationThread(cmd, args)
        self.simulation_thread.output_signal.connect(self.append_log)
        self.simulation_thread.progress_signal.connect(self.progress_bar.setValue)
        self.simulation_thread.finished_signal.connect(self.on_finished)
        self.simulation_thread.start()

    def stop_simulation(self):
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.simulation_thread.stop()
            self.append_log("[SYSTEM] Stopping process...")
            self.stop_btn.setEnabled(False)

    def append_log(self, text):
        self.output_text.append(text)

    def clear_output(self):
        self.output_text.clear()

    def on_finished(self, code):
        self.run_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if code == 0:
            self.status_label.setText("● Completed")
            self.status_label.setObjectName("StatusReady")
            self.append_log("\n[SUCCESS] Simulation finished successfully.")
            QMessageBox.information(self, "完成", "模拟计算已成功完成。")
        else:
            self.status_label.setText("● Error")
            self.status_label.setObjectName("StatusError")
            self.append_log(f"\n[FAILED] Process exited with code {code}.")
        
        # 刷新样式
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # 使用Fusion风格作为基底，更易于跨平台保持一致
    window = Geant4EnterpriseGUI()
    window.show()
    sys.exit(app.exec_())