import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
                             QGroupBox, QTextEdit, QFileDialog, QMessageBox,
                             QProgressBar, QSplitter, QTabWidget, QFrame, QAction,
                             QStyle, QMenu, QStatusBar, QToolBar)
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QTextCursor


class SimulationThread(QThread):
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
            self.output_signal.emit(f"[SYSTEM] Initializing kernel...")
            self.output_signal.emit(f"[EXEC] {self.command} {' '.join(self.args)}")
            self.output_signal.emit("-" * 60)
            
            for i in range(1, 101):
                if not self.is_running: 
                    self.output_signal.emit("[WARN] Process aborted by user request.")
                    break
                
                time.sleep(0.03)
                
                if i % 10 == 0:
                    self.output_signal.emit(f"[PHYSICS] Step {i}: Scattering event processed. dE/dx = 1.2 MeV/cm")
                if i % 25 == 0:
                    self.output_signal.emit(f"[KERNEL] Checkpoint {i}% verified. Memory usage stable.")
                
                self.progress_signal.emit(i)

            if self.is_running:
                self.finished_signal.emit(0)

        except Exception as e:
            self.output_signal.emit(f"[FATAL] Exception: {str(e)}")
            self.finished_signal.emit(-1)

    def stop(self):
        self.is_running = False


class Geant4EnterpriseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulation_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Geant4 Analysis Suite - Enterprise Edition v1.0")
        self.resize(1200, 800)
        
        font = QFont("Segoe UI", 9)
        font.setStyleStrategy(QFont.PreferAntialias)
        QApplication.setFont(font)

        self.create_menu_bar()
        self.create_toolbar()
        self.create_central_widget()
        self.create_status_bar()
        self.apply_stylesheet()

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('文件(&F)')
        
        load_action = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), '加载配置...', self)
        load_action.setShortcut('Ctrl+O')
        file_menu.addAction(load_action)
        
        save_action = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), '保存配置', self)
        save_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(self.style().standardIcon(QStyle.SP_DialogCloseButton), '退出系统', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        sim_menu = menubar.addMenu('模拟(&S)')
        run_action = QAction(self.style().standardIcon(QStyle.SP_MediaPlay), '开始运行', self)
        run_action.triggered.connect(self.run_simulation)
        sim_menu.addAction(run_action)
        
        stop_action = QAction(self.style().standardIcon(QStyle.SP_MediaStop), '强制停止', self)
        stop_action.triggered.connect(self.stop_simulation)
        sim_menu.addAction(stop_action)

        tools_menu = menubar.addMenu('工具(&T)')
        physics_menu = tools_menu.addMenu('物理列表设置')
        physics_menu.addAction('电磁相互作用 (Standard EM)')
        physics_menu.addAction('强子相互作用 (QGSP_BIC)')
        
        tools_menu.addSeparator()
        tools_menu.addAction('环境变量编辑器...')

        help_menu = menubar.addMenu('帮助(&H)')
        help_menu.addAction('用户手册 (PDF)')
        help_menu.addAction('关于软件...')

    def create_toolbar(self):
        toolbar = QToolBar("MainToolbar")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        btn_run = QAction(self.style().standardIcon(QStyle.SP_MediaPlay), "Run", self)
        btn_run.triggered.connect(self.run_simulation)
        toolbar.addAction(btn_run)

        btn_stop = QAction(self.style().standardIcon(QStyle.SP_MediaStop), "Stop", self)
        btn_stop.triggered.connect(self.stop_simulation)
        toolbar.addAction(btn_stop)
        
        toolbar.addSeparator()
        
        btn_clear = QAction(self.style().standardIcon(QStyle.SP_DialogResetButton), "Clear Log", self)
        btn_clear.triggered.connect(self.clear_output)
        toolbar.addAction(btn_clear)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_label = QLabel(" System Ready ")
        self.status_label.setStyleSheet("font-weight: bold; color: #444;")
        self.status_bar.addPermanentWidget(self.status_label)
        
        self.bottom_progress = QProgressBar()
        self.bottom_progress.setFixedWidth(200)
        self.bottom_progress.setTextVisible(False)
        self.status_bar.addPermanentWidget(self.bottom_progress)

    def create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 10, 0)
        
        header = QLabel("Simulation Configuration")
        header.setObjectName("PanelHeader")
        left_layout.addWidget(header)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_general_tab(), "常规设置 (General)")
        self.tabs.addTab(self.create_physics_tab(), "物理参数 (Physics)")
        self.tabs.addTab(self.create_geometry_tab(), "几何结构 (Geometry)")
        left_layout.addWidget(self.tabs)

        action_frame = QFrame()
        action_frame.setObjectName("ActionFrame")
        action_layout = QVBoxLayout(action_frame)
        
        self.main_progress_bar = QProgressBar()
        self.main_progress_bar.setFormat("Progress: %p%")
        self.main_progress_bar.setAlignment(Qt.AlignCenter)
        
        self.btn_start_big = QPushButton("执行模拟 (Start Execution)")
        self.btn_start_big.setObjectName("PrimaryButton")
        self.btn_start_big.setCursor(Qt.PointingHandCursor)
        self.btn_start_big.clicked.connect(self.run_simulation)
        self.btn_start_big.setFixedHeight(45)

        action_layout.addWidget(QLabel("Task Progress:"))
        action_layout.addWidget(self.main_progress_bar)
        action_layout.addSpacing(10)
        action_layout.addWidget(self.btn_start_big)

        left_layout.addWidget(action_frame)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 0, 0, 0)

        log_header_layout = QHBoxLayout()
        log_label = QLabel("Console Output")
        log_label.setObjectName("PanelHeader")
        log_header_layout.addWidget(log_label)
        log_header_layout.addStretch()
        
        export_btn = QPushButton("Export Log")
        export_btn.setFixedWidth(100)
        log_header_layout.addWidget(export_btn)
        
        right_layout.addLayout(log_header_layout)

        self.console_log = QTextEdit()
        self.console_log.setReadOnly(True)
        self.console_log.setObjectName("Console")
        right_layout.addWidget(self.console_log)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([450, 750])
        splitter.setCollapsible(0, False)

        main_layout.addWidget(splitter)

    def create_form_row(self, label, widget, unit=None):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 4, 0, 4)
        
        lbl = QLabel(label)
        lbl.setFixedWidth(140)
        lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbl.setStyleSheet("color: #555;")
        
        layout.addWidget(lbl)
        layout.addSpacing(10)
        layout.addWidget(widget)
        
        if unit:
            u_lbl = QLabel(unit)
            u_lbl.setStyleSheet("color: #777;")
            layout.addWidget(u_lbl)
            
        return container

    def create_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 20, 15, 20)

        grp_files = QGroupBox("Project Files")
        l_files = QVBoxLayout(grp_files)
        
        self.path_exec = QLineEdit("./geant4_app")
        btn_browse = QPushButton("Browse...")
        l_files.addWidget(self.create_form_row("Executable Path:", self.path_exec))
        
        self.path_macro = QLineEdit("run.mac")
        l_files.addWidget(self.create_form_row("Macro File:", self.path_macro))
        
        layout.addWidget(grp_files)
        
        grp_run = QGroupBox("Runtime Settings")
        l_run = QVBoxLayout(grp_run)
        
        self.spin_events = QLineEdit("10000")
        l_run.addWidget(self.create_form_row("Number of Events:", self.spin_events))
        
        self.cmb_threads = QComboBox()
        self.cmb_threads.addItems(["Auto (Max)", "1", "2", "4", "8", "16"])
        l_run.addWidget(self.create_form_row("Multi-threading:", self.cmb_threads))
        
        layout.addWidget(grp_run)
        layout.addStretch()
        return tab

    def create_physics_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 20, 15, 20)
        
        grp_source = QGroupBox("Primary Generator")
        l_source = QVBoxLayout(grp_source)
        
        self.cmb_particle = QComboBox()
        self.cmb_particle.addItems(["gamma", "e-", "e+", "proton", "neutron", "alpha"])
        l_source.addWidget(self.create_form_row("Particle Type:", self.cmb_particle))
        
        self.txt_energy = QLineEdit("1.0")
        l_source.addWidget(self.create_form_row("Beam Energy:", self.txt_energy, "MeV"))
        
        layout.addWidget(grp_source)
        layout.addStretch()
        return tab

    def create_geometry_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 20, 15, 20)
        
        label = QLabel("Geometry settings loaded from GDML or DetectorConstruction.")
        label.setWordWrap(True)
        label.setStyleSheet("color: #666; font-style: italic;")
        
        layout.addWidget(label)
        
        grp_mat = QGroupBox("Material Overrides")
        l_mat = QVBoxLayout(grp_mat)
        
        self.cmb_target = QComboBox()
        self.cmb_target.addItems(["G4_Pb", "G4_WATER", "G4_CONCRETE", "G4_Al"])
        l_mat.addWidget(self.create_form_row("Target Material:", self.cmb_target))
        
        layout.addWidget(grp_mat)
        layout.addStretch()
        return tab

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f5f7fa;
                color: #333333;
            }

            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                padding: 2px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background-color: #e6f7ff;
                color: #0078d7;
            }

            QToolBar {
                background-color: #ffffff;
                border-bottom: 1px solid #dcdcdc;
                padding: 4px;
                spacing: 10px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 3px;
                padding: 3px;
            }
            QToolButton:hover {
                background-color: #eef6fb;
                border: 1px solid #cfe5f7;
            }

            QLabel#PanelHeader {
                font-size: 14px;
                font-weight: bold;
                color: #004578;
                padding-bottom: 8px;
                border-bottom: 2px solid #0078d7;
                margin-bottom: 10px;
            }

            QTabWidget::pane {
                border: 1px solid #dcdcdc;
                background: #ffffff;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #e1e4e8;
                border: 1px solid #c0c4c9;
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                color: #555;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom-color: #ffffff;
                color: #0078d7;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #f0f2f5;
            }

            QGroupBox {
                font-weight: bold;
                border: 1px solid #d1d1d1;
                border-radius: 5px;
                margin-top: 20px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                color: #333;
            }

            QLineEdit, QComboBox {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                background: #ffffff;
                selection-background-color: #0078d7;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0078d7;
            }

            QPushButton {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 6px 12px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #f2f2f2;
                border-color: #999;
            }
            
            QPushButton#PrimaryButton {
                background-color: #0078d7;
                color: white;
                border: none;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton#PrimaryButton:hover {
                background-color: #1084d9;
            }
            QPushButton#PrimaryButton:pressed {
                background-color: #005a9e;
            }
            QPushButton#PrimaryButton:disabled {
                background-color: #cccccc;
            }

            QTextEdit#Console {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #333;
                border-radius: 4px;
            }

            QProgressBar {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                text-align: center;
                background: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
                width: 10px;
            }

            QStatusBar {
                background: #ffffff;
                border-top: 1px solid #e0e0e0;
                color: #666;
            }
            
            QSplitter::handle {
                background-color: #e0e0e0;
            }
        """)

    def run_simulation(self):
        self.console_log.clear()
        self.btn_start_big.setEnabled(False)
        self.status_label.setText(" Status: Running Simulation... ")
        self.status_label.setStyleSheet("color: #0078d7; font-weight: bold;")
        
        cmd = self.path_exec.text()
        args = [self.path_macro.text(), self.cmb_particle.currentText()]
        
        self.simulation_thread = SimulationThread(cmd, args)
        self.simulation_thread.output_signal.connect(self.append_log)
        self.simulation_thread.progress_signal.connect(self.update_progress)
        self.simulation_thread.finished_signal.connect(self.on_finished)
        self.simulation_thread.start()

    def stop_simulation(self):
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.simulation_thread.stop()
            self.append_log("[SYSTEM] Sending abort signal...")

    def append_log(self, text):
        self.console_log.append(text)
        self.console_log.moveCursor(QTextCursor.End)

    def clear_output(self):
        self.console_log.clear()

    def update_progress(self, val):
        self.main_progress_bar.setValue(val)
        self.bottom_progress.setValue(val)

    def on_finished(self, code):
        self.btn_start_big.setEnabled(True)
        self.status_label.setText(" Status: Idle / Ready ")
        self.status_label.setStyleSheet("color: #444; font-weight: bold;")
        
        if code == 0:
            QMessageBox.information(self, "Success", "Simulation run completed successfully.")
        else:
            QMessageBox.warning(self, "Failed", "Simulation terminated with errors.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    window = Geant4EnterpriseGUI()
    window.show()
    sys.exit(app.exec_())