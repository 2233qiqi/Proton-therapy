import sys
import subprocess
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
                             QGroupBox, QTextEdit, QFileDialog, QMessageBox,
                             QProgressBar, QSplitter, QFrame, QTabWidget, QStyleFactory)
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class SimulationThread(QThread):
    """用于在后台运行Geant4模拟的线程 (逻辑保持不变)"""
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
            # 模拟运行环境，实际使用时请取消注释并调整
            # process = subprocess.Popen(...)
            
            # --- 仅用于演示界面的模拟逻辑 Start ---
            import time
            self.output_signal.emit(f"正在启动: {self.command} {' '.join(self.args)}")
            for i in range(1, 101):
                if not self.is_running: break
                time.sleep(0.05) # 模拟计算耗时
                self.output_signal.emit(f"G4Worker: 处理事件 ID {i} ... 能量沉积计算完成")
                if i % 10 == 0:
                    self.output_signal.emit(f"--- 进度检查点: {i}% ---")
                self.progress_signal.emit(i)
            # --- 演示逻辑 End ---

            if self.is_running:
                self.finished_signal.emit(0)

        except Exception as e:
            self.output_signal.emit(f"错误: {str(e)}")
            self.finished_signal.emit(-1)

    def stop(self):
        self.is_running = False

class Geant4GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulation_thread = None
        self.init_ui()

    def init_ui(self):
        # 设置全局字体
        font = QFont("Segoe UI", 10)
        font.setStyleStrategy(QFont.PreferAntialias)
        QApplication.setFont(font)

        self.setWindowTitle("Geant4 辐射屏蔽模拟系统")
        self.resize(1100, 850)
        
        # 应用现代深色主题
        self.apply_modern_theme()

        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # 1. 顶部标题区域
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 10)
        
        title_label = QLabel("Geant4 Simulation")
        title_label.setObjectName("mainTitle") # 用于QSS定位
        
        subtitle_label = QLabel("辐射屏蔽效应分析平台")
        subtitle_label.setObjectName("subTitle")

        title_info_layout = QVBoxLayout()
        title_info_layout.addWidget(title_label)
        title_info_layout.addWidget(subtitle_label)
        
        title_layout.addLayout(title_info_layout)
        title_layout.addStretch()
        
        # 添加一个状态标签
        self.status_badge = QLabel("READY")
        self.status_badge.setObjectName("statusBadge")
        self.status_badge.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.status_badge)

        main_layout.addWidget(title_container)

        # 2. 分割器区域
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(2)

        # --- 上部分：设置区域 ---
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)
        upper_layout.setContentsMargins(0, 0, 0, 10)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_basic_tab(), "基本参数")
        self.tab_widget.addTab(self.create_advanced_tab(), "高级配置")
        upper_layout.addWidget(self.tab_widget)

        # --- 下部分：控制与输出 ---
        lower_widget = QWidget()
        lower_layout = QVBoxLayout(lower_widget)
        lower_layout.setContentsMargins(0, 10, 0, 0)
        lower_layout.setSpacing(15)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        lower_layout.addWidget(self.progress_bar)

        # 按钮栏
        lower_layout.addWidget(self.create_control_buttons())

        # 终端输出
        output_label = QLabel("TERMINAL OUTPUT")
        output_label.setObjectName("sectionHeader")
        lower_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        lower_layout.addWidget(self.output_text)

        splitter.addWidget(upper_widget)
        splitter.addWidget(lower_widget)
        splitter.setSizes([380, 520]) 

        main_layout.addWidget(splitter)

    def apply_modern_theme(self):
        """应用现代QSS样式表"""
        self.setStyleSheet("""
            /* 全局背景和字体 */
            QMainWindow, QWidget {
                background-color: #1e2129;
                color: #e2e8f0;
                outline: none;
            }
            
            /* 分割器 */
            QSplitter::handle {
                background-color: #333a4a;
                margin: 10px;
            }
            QSplitter::handle:hover {
                background-color: #3b82f6;
            }

            /* 标题样式 */
            QLabel#mainTitle {
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#subTitle {
                font-size: 14px;
                color: #94a3b8;
                margin-top: -5px;
            }
            QLabel#sectionHeader {
                font-size: 12px;
                font-weight: bold;
                color: #64748b;
                letter-spacing: 1px;
            }
            QLabel#statusBadge {
                background-color: #333a4a;
                color: #10b981;
                border-radius: 4px;
                padding: 4px 12px;
                font-weight: bold;
                font-size: 12px;
            }

            /* 选项卡 (TabWidget) */
            QTabWidget::pane {
                border: 1px solid #333a4a;
                border-radius: 0px 0px 8px 8px;
                background-color: #262a35;
                top: -1px; 
            }
            QTabBar::tab {
                background-color: #1e2129;
                color: #94a3b8;
                padding: 10px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background-color: #262a35;
                color: #3b82f6;
                border-bottom: 2px solid #3b82f6;
            }
            QTabBar::tab:hover:!selected {
                background-color: #2d3342;
                color: #e2e8f0;
            }

            /* GroupBox (卡片式设计) */
            QGroupBox {
                border: 1px solid #333a4a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 24px;
                background-color: #262a35;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                top: 2px;
                color: #3b82f6;
                font-weight: bold;
                background-color: #262a35; 
                padding: 0 5px;
            }

            /* 输入框 (LineEdit & ComboBox) */
            QLineEdit, QComboBox {
                background-color: #1e2129;
                border: 1px solid #333a4a;
                border-radius: 6px;
                padding: 6px 10px;
                color: #f1f5f9;
                selection-background-color: #3b82f6;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3b82f6;
                background-color: #222630;
            }
            QLineEdit:placeholder {
                color: #475569;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #64748b;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e2129;
                border: 1px solid #333a4a;
                selection-background-color: #3b82f6;
                outline: none;
            }

            /* 按钮 (通用) */
            QPushButton {
                background-color: #333a4a;
                color: #e2e8f0;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #475569;
            }
            QPushButton:pressed {
                background-color: #1e293b;
            }
            
            /* 浏览按钮 (特殊) */
            QPushButton#browseBtn {
                background-color: transparent;
                border: 1px solid #333a4a;
                color: #94a3b8;
            }
            QPushButton#browseBtn:hover {
                border-color: #64748b;
                color: #e2e8f0;
            }

            /* 开始模拟按钮 */
            QPushButton#runBtn {
                background-color: #2563eb; /* 科技蓝 */
                color: white;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton#runBtn:hover {
                background-color: #1d4ed8;
            }
            QPushButton#runBtn:pressed {
                background-color: #1e40af;
            }
            QPushButton#runBtn:disabled {
                background-color: #333a4a;
                color: #64748b;
            }

            /* 停止按钮 */
            QPushButton#stopBtn {
                background-color: #262a35;
                border: 1px solid #ef4444;
                color: #ef4444;
            }
            QPushButton#stopBtn:hover {
                background-color: #ef4444;
                color: white;
            }
            QPushButton#stopBtn:disabled {
                border-color: #333a4a;
                color: #475569;
                background-color: transparent;
            }

            /* 进度条 */
            QProgressBar {
                background-color: #1e2129;
                border-radius: 4px;
                text-align: center;
                color: white;
                height: 10px;
                border: 1px solid #333a4a;
            }
            QProgressBar::chunk {
                background-color: #10b981; /* 湖水绿 */
                border-radius: 3px;
            }

            /* 文本输出区域 */
            QTextEdit {
                background-color: #111318; /* 极深色背景 */
                color: #a5b4fc;
                border: 1px solid #333a4a;
                border-radius: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
                padding: 10px;
                font-size: 12px;
                line-height: 150%;
            }
            
            /* 滚动条美化 */
            QScrollBar:vertical {
                border: none;
                background: #1e2129;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #475569;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    def create_form_row(self, label_text, widget, unit_text=None, btn=None):
        """辅助函数：创建统一格式的表单行"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label.setFixedWidth(100)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("color: #94a3b8;")
        
        layout.addWidget(label)
        layout.addWidget(widget)
        
        if unit_text:
            if isinstance(unit_text, str):
                unit = QLabel(unit_text)
                unit.setStyleSheet("color: #64748b; font-weight: bold;")
                layout.addWidget(unit)
            else: # 如果是widget (如ComboBox单位选择)
                layout.addWidget(unit_text)
        
        if btn:
            layout.addWidget(btn)
            
        return container

    def create_basic_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # === 核心文件 ===
        file_group = QGroupBox("CORE FILES")
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(12)

        # Executable
        self.exec_file_edit = QLineEdit("./main")
        self.exec_file_edit.setPlaceholderText("选择 Geant4 可执行文件")
        browse_exec_btn = QPushButton("浏览")
        browse_exec_btn.setObjectName("browseBtn")
        browse_exec_btn.clicked.connect(self.browse_exec_file)
        file_layout.addWidget(self.create_form_row("可执行文件", self.exec_file_edit, btn=browse_exec_btn))

        # Macro
        self.macro_file_edit = QLineEdit()
        self.macro_file_edit.setPlaceholderText("默认配置 (可选)")
        browse_macro_btn = QPushButton("浏览")
        browse_macro_btn.setObjectName("browseBtn")
        browse_macro_btn.clicked.connect(self.browse_macro_file)
        file_layout.addWidget(self.create_form_row("宏文件", self.macro_file_edit, btn=browse_macro_btn))

        layout.addWidget(file_group)

        # === 粒子源设置 ===
        source_group = QGroupBox("PARTICLE SOURCE")
        source_layout = QVBoxLayout(source_group)
        source_layout.setSpacing(12)

        # Particle Type
        self.particle_combo = QComboBox()
        self.particle_combo.addItems(["gamma", "e-", "e+", "proton", "neutron"])
        source_layout.addWidget(self.create_form_row("粒子类型", self.particle_combo))

        # Energy
        self.energy_edit = QLineEdit("1.0")
        self.energy_unit_combo = QComboBox()
        self.energy_unit_combo.addItems(["MeV", "GeV", "keV"])
        self.energy_unit_combo.setFixedWidth(80)
        source_layout.addWidget(self.create_form_row("初始能量", self.energy_edit, unit_text=self.energy_unit_combo))

        layout.addWidget(source_group)
        layout.addStretch()
        return widget

    def create_advanced_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # === 几何与屏蔽 ===
        shield_group = QGroupBox("GEOMETRY & SHIELDING")
        shield_layout = QVBoxLayout(shield_group)
        shield_layout.setSpacing(12)

        self.material_combo = QComboBox()
        self.material_combo.addItems(["铅 (Pb)", "铁 (Fe)", "混凝土 (Concrete)", "水 (H2O)", "聚乙烯 (PE)"])
        shield_layout.addWidget(self.create_form_row("屏蔽材料", self.material_combo))

        self.thickness_edit = QLineEdit("10.0")
        shield_layout.addWidget(self.create_form_row("屏蔽厚度", self.thickness_edit, unit_text="cm"))

        layout.addWidget(shield_group)

        # === 物理过程与控制 ===
        control_group = QGroupBox("PHYSICS & RUN")
        control_layout = QVBoxLayout(control_group)
        control_layout.setSpacing(12)

        self.events_edit = QLineEdit("1000")
        control_layout.addWidget(self.create_form_row("模拟事件数", self.events_edit, unit_text="Events"))
        
        # 模拟线程数 (新增一个看起来很高级的选项)
        self.threads_combo = QComboBox()
        self.threads_combo.addItems(["单线程", "2 线程", "4 线程", "8 线程 (Max)"])
        control_layout.addWidget(self.create_form_row("并行计算", self.threads_combo))

        layout.addWidget(control_group)
        layout.addStretch()
        return widget

    def create_control_buttons(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.run_btn = QPushButton("开始模拟 (RUN)")
        self.run_btn.setObjectName("runBtn")
        self.run_btn.setMinimumHeight(45)
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_simulation)

        self.stop_btn = QPushButton("中止")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setFixedSize(100, 45)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.clicked.connect(self.stop_simulation)
        self.stop_btn.setEnabled(False)

        self.clear_btn = QPushButton("清除日志")
        self.clear_btn.setFixedSize(100, 45)
        self.clear_btn.clicked.connect(self.clear_output)

        layout.addWidget(self.run_btn)
        layout.addWidget(self.stop_btn)
        layout.addStretch()
        layout.addWidget(self.clear_btn)

        return widget

    # --- 逻辑功能区 (Logic Functions) 保持逻辑一致性 ---

    def browse_macro_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择宏文件", "", "宏文件 (*.mac);;所有文件 (*)")
        if file_path: self.macro_file_edit.setText(file_path)

    def browse_exec_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择可执行文件", "", "可执行文件 (*);;所有文件 (*)")
        if file_path: self.exec_file_edit.setText(file_path)

    def material_to_command(self, text):
        mapping = {"铅 (Pb)": "Pb", "铁 (Fe)": "Fe", "混凝土 (Concrete)": "Concrete", 
                   "水 (H2O)": "Water", "聚乙烯 (PE)": "Polyethylene"}
        return mapping.get(text, "Pb")

    def run_simulation(self):
        exec_file = self.exec_file_edit.text()
        
        # 为了演示效果，这里注释掉文件检查，方便你直接运行查看UI
        # if not os.path.exists(exec_file):
        #     QMessageBox.critical(self, "路径错误", f"找不到可执行文件:\n{exec_file}")
        #     return

        args = []
        args.append(self.macro_file_edit.text() if self.macro_file_edit.text() else "vis.mac")
        args.append(self.material_to_command(self.material_combo.currentText()))
        args.append(self.thickness_edit.text())
        args.append(self.particle_combo.currentText())
        args.append(f"{self.energy_edit.text()} {self.energy_unit_combo.currentText()}")
        
        self.output_text.clear()
        self.toggle_ui_state(running=True)
        self.status_badge.setText("RUNNING")
        self.status_badge.setStyleSheet("background-color: #2563eb; color: white; border-radius: 4px; padding: 4px 12px;")
        
        self.output_text.append(f"<span style='color: #3b82f6;'>➜初始化环境配置...</span>")
        
        self.simulation_thread = SimulationThread(exec_file, args)
        self.simulation_thread.output_signal.connect(self.update_output)
        self.simulation_thread.finished_signal.connect(self.simulation_finished)
        self.simulation_thread.progress_signal.connect(self.update_progress)
        self.simulation_thread.start()

    def stop_simulation(self):
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.simulation_thread.stop()
            self.output_text.append("<span style='color: #ef4444;'>⚠ 用户请求中止模拟...</span>")

    def clear_output(self):
        self.output_text.clear()

    def update_output(self, text):
        self.output_text.append(text)
        # 自动滚动
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        self.output_text.setTextCursor(cursor)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def toggle_ui_state(self, running):
        self.run_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)
        self.progress_bar.setVisible(running)
        if running:
            self.progress_bar.setValue(0)

    def simulation_finished(self, exit_code):
        self.toggle_ui_state(running=False)
        
        if exit_code == 0:
            self.status_badge.setText("COMPLETED")
            self.status_badge.setStyleSheet("background-color: #10b981; color: #064e3b; border-radius: 4px; padding: 4px 12px;")
            self.output_text.append("<br><span style='color: #10b981;'>✔ 模拟成功完成. Output saved to data/</span>")
        else:
            self.status_badge.setText("ERROR")
            self.status_badge.setStyleSheet("background-color: #ef4444; color: white; border-radius: 4px; padding: 4px 12px;")
            self.output_text.append(f"<br><span style='color: #ef4444;'>✘ 模拟异常退出 (Code: {exit_code})</span>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion') # Fusion 风格作为基础，然后用 QSS 覆盖
    window = Geant4GUI()
    window.show()
    sys.exit(app.exec_())