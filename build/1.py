import sys
import subprocess
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
                             QGroupBox, QTextEdit, QFileDialog, QMessageBox,
                             QProgressBar, QSplitter, QFrame, QTabWidget)
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon


class SimulationThread(QThread):
    """用于在后台运行Geant4模拟的线程"""

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
            # 运行Geant4模拟程序
            process = subprocess.Popen(
                [self.command] + self.args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # 实时输出
            line_count = 0
            for line in process.stdout:
                if not self.is_running:
                    break
                self.output_signal.emit(line.strip())
                line_count += 1
                # 每10行更新一次进度（模拟进度效果）
                if line_count % 10 == 0:
                    self.progress_signal.emit(min(90, line_count // 10))

            if self.is_running:
                process.wait()
                self.progress_signal.emit(100)
                self.finished_signal.emit(process.returncode)

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
        QApplication.setFont(QFont("Noto Sans CJK SC", 10))

        self.setWindowTitle("Geant4 辐射屏蔽模拟系统")
        self.setGeometry(100, 100, 1200, 900)
        
        # 设置应用样式 
        self.set_dark_theme()

        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 创建标题
        title_label = QLabel("Geant4 辐射屏蔽模拟系统")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                color: #4fc3f7;
                padding: 25px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e1e1e, stop:0.5 #2d2d2d, stop:1 #1e1e1e);
                border-radius: 12px;
                margin-bottom: 15px;
                border: 2px solid #404040;
            }
        """)
        main_layout.addWidget(title_label)

        # 创建分割器，使界面可以调整大小
        splitter = QSplitter(Qt.Vertical)

        # 创建上部分 - 参数设置区域
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)
        upper_layout.setContentsMargins(5, 5, 5, 5)
        upper_layout.setSpacing(10)

        # 使用选项卡组织参数设置
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #404040;
                border-radius: 8px;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #e0e0e0;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #1976d2;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #555555;
            }
        """)

        # 基本设置选项卡
        basic_tab = self.create_basic_tab()
        tab_widget.addTab(basic_tab, "基本设置")

        # 高级设置选项卡
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "高级设置")

        upper_layout.addWidget(tab_widget)

        # 创建下部分 - 输出和控制区域
        lower_widget = QWidget()
        lower_layout = QVBoxLayout(lower_widget)
        lower_layout.setContentsMargins(5, 5, 5, 5)
        lower_layout.setSpacing(12)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 8px;
                text-align: center;
                background-color: #2d2d2d;
                height: 24px;
                font-weight: bold;
                color: #e0e0e0;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00c853, stop:1 #009624);
                border-radius: 6px;
            }
        """)
        self.progress_bar.setVisible(False)
        lower_layout.addWidget(self.progress_bar)

        # 控制按钮
        control_widget = self.create_control_buttons()
        lower_layout.addWidget(control_widget)

        # 输出显示
        output_group = QGroupBox("模拟输出")
        output_group.setStyleSheet(self.get_groupbox_style())
        output_layout = QVBoxLayout(output_group)
        output_layout.setContentsMargins(12, 20, 12, 12)
        output_layout.setSpacing(8)

        self.output_text = QTextEdit()
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #76ff03;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 12px;
                selection-background-color: #1976d2;
            }
        """)
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)

        lower_layout.addWidget(output_group)

        # 将上下部分添加到分割器
        splitter.addWidget(upper_widget)
        splitter.addWidget(lower_widget)
        splitter.setSizes([400, 500])

        main_layout.addWidget(splitter)

    def create_basic_tab(self):
        """创建基本设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # 执行文件设置
        exec_group = QGroupBox("执行文件设置")
        exec_group.setStyleSheet(self.get_groupbox_style())
        exec_layout = QVBoxLayout(exec_group)
        exec_layout.setContentsMargins(15, 20, 15, 15)
        exec_layout.setSpacing(12)

        exec_file_layout = QHBoxLayout()
        exec_file_layout.setSpacing(10)
        exec_file_label = QLabel("可执行文件:")
        exec_file_label.setFixedWidth(100)  # 固定标签宽度
        exec_file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.exec_file_edit = QLineEdit("./main")
        self.exec_file_edit.setStyleSheet(self.get_lineedit_style())
        self.exec_file_edit.setPlaceholderText("选择 Geant4 可执行文件路径...")
        browse_exec_btn = QPushButton("浏览")
        browse_exec_btn.setStyleSheet(self.get_button_style())
        browse_exec_btn.setFixedWidth(80)  # 固定按钮宽度
        browse_exec_btn.clicked.connect(self.browse_exec_file)

        exec_file_layout.addWidget(exec_file_label)
        exec_file_layout.addWidget(self.exec_file_edit)
        exec_file_layout.addWidget(browse_exec_btn)
        exec_layout.addLayout(exec_file_layout)

        layout.addWidget(exec_group)

        # 宏文件设置
        macro_group = QGroupBox("宏文件设置")
        macro_group.setStyleSheet(self.get_groupbox_style())
        macro_layout = QVBoxLayout(macro_group)
        macro_layout.setContentsMargins(15, 20, 15, 15)
        macro_layout.setSpacing(12)

        macro_file_layout = QHBoxLayout()
        macro_file_layout.setSpacing(10)
        macro_file_label = QLabel("宏文件:")
        macro_file_label.setFixedWidth(100)  # 固定标签宽度
        macro_file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.macro_file_edit = QLineEdit()
        self.macro_file_edit.setStyleSheet(self.get_lineedit_style())
        self.macro_file_edit.setPlaceholderText("选择宏文件 (.mac)...")
        browse_macro_btn = QPushButton("浏览")
        browse_macro_btn.setStyleSheet(self.get_button_style())
        browse_macro_btn.setFixedWidth(80)  # 固定按钮宽度
        browse_macro_btn.clicked.connect(self.browse_macro_file)

        macro_file_layout.addWidget(macro_file_label)
        macro_file_layout.addWidget(self.macro_file_edit)
        macro_file_layout.addWidget(browse_macro_btn)
        macro_layout.addLayout(macro_file_layout)

        layout.addWidget(macro_group)

        # 粒子源参数
        source_group = QGroupBox("粒子源参数")
        source_group.setStyleSheet(self.get_groupbox_style())
        source_layout = QVBoxLayout(source_group)
        source_layout.setContentsMargins(15, 20, 15, 15)
        source_layout.setSpacing(15)

        # 粒子类型
        particle_layout = QHBoxLayout()
        particle_layout.setSpacing(10)
        particle_label = QLabel("粒子类型:")
        particle_label.setFixedWidth(100)  # 固定标签宽度
        particle_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.particle_combo = QComboBox()
        self.particle_combo.setStyleSheet(self.get_combobox_style())
        self.particle_combo.addItems(["gamma", "e-", "e+", "proton", "neutron"])
        self.particle_combo.setFixedHeight(35)  # 固定高度

        particle_layout.addWidget(particle_label)
        particle_layout.addWidget(self.particle_combo)
        particle_layout.addStretch()  # 添加弹性空间
        source_layout.addLayout(particle_layout)

        # 能量设置
        energy_layout = QHBoxLayout()
        energy_layout.setSpacing(10)
        energy_label = QLabel("能量:")
        energy_label.setFixedWidth(100)  # 固定标签宽度
        energy_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.energy_edit = QLineEdit("1.0")
        self.energy_edit.setStyleSheet(self.get_lineedit_style())
        self.energy_edit.setPlaceholderText("输入能量值")
        self.energy_edit.setFixedHeight(35)  # 固定高度
        self.energy_unit_combo = QComboBox()
        self.energy_unit_combo.setStyleSheet(self.get_combobox_style())
        self.energy_unit_combo.addItems(["MeV", "GeV", "keV"])
        self.energy_unit_combo.setFixedHeight(35)  # 固定高度
        self.energy_unit_combo.setFixedWidth(100)  # 固定宽度

        energy_layout.addWidget(energy_label)
        energy_layout.addWidget(self.energy_edit)
        energy_layout.addWidget(self.energy_unit_combo)
        energy_layout.addStretch()  # 添加弹性空间
        source_layout.addLayout(energy_layout)

        layout.addWidget(source_group)
        layout.addStretch()  # 添加弹性空间使内容顶部对齐

        return widget

    def create_advanced_tab(self):
        """创建高级设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # 屏蔽层参数
        shield_group = QGroupBox("屏蔽层参数")
        shield_group.setStyleSheet(self.get_groupbox_style())
        shield_layout = QVBoxLayout(shield_group)
        shield_layout.setContentsMargins(15, 20, 15, 15)
        shield_layout.setSpacing(15)

        # 材料选择
        material_layout = QHBoxLayout()
        material_layout.setSpacing(10)
        material_label = QLabel("屏蔽材料:")
        material_label.setFixedWidth(100)  # 固定标签宽度
        material_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.material_combo = QComboBox()
        self.material_combo.setStyleSheet(self.get_combobox_style())
        self.material_combo.addItems(["铅", "铁", "混凝土", "水", "聚乙烯"])
        self.material_combo.setFixedHeight(35)  # 固定高度

        material_layout.addWidget(material_label)
        material_layout.addWidget(self.material_combo)
        material_layout.addStretch()  # 添加弹性空间
        shield_layout.addLayout(material_layout)

        # 厚度设置
        thickness_layout = QHBoxLayout()
        thickness_layout.setSpacing(10)
        thickness_label = QLabel("厚度:")
        thickness_label.setFixedWidth(100)  # 固定标签宽度
        thickness_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.thickness_edit = QLineEdit("10")
        self.thickness_edit.setStyleSheet(self.get_lineedit_style())
        self.thickness_edit.setPlaceholderText("输入厚度值")
        self.thickness_edit.setFixedHeight(35)  # 固定高度
        thickness_unit_label = QLabel("cm")
        thickness_unit_label.setFixedWidth(30)  # 固定单位标签宽度

        thickness_layout.addWidget(thickness_label)
        thickness_layout.addWidget(self.thickness_edit)
        thickness_layout.addWidget(thickness_unit_label)
        thickness_layout.addStretch()  # 添加弹性空间
        shield_layout.addLayout(thickness_layout)

        layout.addWidget(shield_group)

        # 模拟控制参数
        control_group = QGroupBox("模拟控制")
        control_group.setStyleSheet(self.get_groupbox_style())
        control_layout = QVBoxLayout(control_group)
        control_layout.setContentsMargins(15, 20, 15, 15)
        control_layout.setSpacing(15)

        # 事件数设置
        events_layout = QHBoxLayout()
        events_layout.setSpacing(10)
        events_label = QLabel("事件数量:")
        events_label.setFixedWidth(100)  # 固定标签宽度
        events_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.events_edit = QLineEdit("1000")
        self.events_edit.setStyleSheet(self.get_lineedit_style())
        self.events_edit.setPlaceholderText("输入事件数量")
        self.events_edit.setFixedHeight(35)  # 固定高度

        events_layout.addWidget(events_label)
        events_layout.addWidget(self.events_edit)
        events_layout.addStretch()  # 添加弹性空间
        control_layout.addLayout(events_layout)

        layout.addWidget(control_group)
        layout.addStretch()  # 添加弹性空间使内容顶部对齐

        return widget

    def create_control_buttons(self):
        """创建控制按钮区域"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.run_btn = QPushButton("开始模拟")
        self.run_btn.setStyleSheet(self.get_run_button_style())
        self.run_btn.setFixedHeight(45)  # 固定按钮高度
        self.run_btn.clicked.connect(self.run_simulation)

        self.stop_btn = QPushButton("停止模拟")
        self.stop_btn.setStyleSheet(self.get_stop_button_style())
        self.stop_btn.setFixedHeight(45)  # 固定按钮高度
        self.stop_btn.clicked.connect(self.stop_simulation)
        self.stop_btn.setEnabled(False)

        self.clear_btn = QPushButton("清空输出")
        self.clear_btn.setStyleSheet(self.get_button_style())
        self.clear_btn.setFixedHeight(45)  # 固定按钮高度
        self.clear_btn.clicked.connect(self.clear_output)

        layout.addWidget(self.run_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.clear_btn)
        layout.addStretch()

        return widget

    def set_dark_theme(self):
        """设置现代化的深色主题"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
        """)

    def get_groupbox_style(self):
        """获取GroupBox样式"""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #ffffff;
                border: 2px solid #404040;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: #2d2d2d;
                padding-bottom: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 12px 0 12px;
                color: #4fc3f7;
                background-color: #2d2d2d;
                font-size: 13px;
                font-weight: bold;
            }
        """

    def get_button_style(self):
        """获取普通按钮样式"""
        return """
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-width: 90px;
                transition: background-color 0.2s;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
                padding: 11px 18px 9px 18px;
            }
            QPushButton:disabled {
                background-color: #424242;
                color: #9e9e9e;
            }
        """

    def get_run_button_style(self):
        """获取运行按钮样式"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00c853, stop:1 #00a844);
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00b34a, stop:1 #00963a);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00963a, stop:1 #007a30);
                padding: 13px 25px 11px 25px;
            }
            QPushButton:disabled {
                background-color: #424242;
                color: #9e9e9e;
            }
        """

    def get_stop_button_style(self):
        """获取停止按钮样式"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff4444, stop:1 #cc3333);
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff3333, stop:1 #bb2222);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bb2222, stop:1 #991111);
                padding: 13px 25px 11px 25px;
            }
            QPushButton:disabled {
                background-color: #424242;
                color: #9e9e9e;
            }
        """

    def get_lineedit_style(self):
        """获取输入框样式"""
        return """
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 13px;
                selection-background-color: #1976d2;
            }
            QLineEdit:focus {
                border-color: #1976d2;
                background-color: #252525;
            }
            QLineEdit:placeholder {
                color: #9e9e9e;
                font-style: italic;
            }
        """

    def get_combobox_style(self):
        """获取下拉框样式"""
        return """
            QComboBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 10px 12px;
                min-width: 120px;
                font-size: 13px;
            }
            QComboBox:focus {
                border-color: #1976d2;
                background-color: #252525;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #e0e0e0;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                color: #e0e0e0;
                selection-background-color: #1976d2;
                outline: none;
            }
        """

    def browse_macro_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择宏文件", "", "宏文件 (*.mac);;所有文件 (*)"
        )
        if file_path:
            self.macro_file_edit.setText(file_path)

    def browse_exec_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择可执行文件", "", "可执行文件 (*);;所有文件 (*)"
        )
        if file_path:
            self.exec_file_edit.setText(file_path)

    def material_to_command(self, material):
        """将材料名称转换为Geant4命令字符串"""
        material_map = {
            "铅": "Pb",
            "铁": "Fe",
            "混凝土": "Concrete",
            "水": "Water",
            "聚乙烯": "Polyethylene"
        }
        return material_map.get(material, "Pb")

    def run_simulation(self):
        """运行模拟"""
        # 检查可执行文件是否存在
        exec_file = self.exec_file_edit.text()
        if not os.path.exists(exec_file):
            QMessageBox.critical(self, "错误", f"可执行文件不存在: {exec_file}")
            return

        # 构建参数列表
        args = []

        # 宏文件
        macro_file = self.macro_file_edit.text()
        if macro_file:
            args.append(macro_file)
        else:
            args.append("")

        # 材料参数
        material = self.material_to_command(self.material_combo.currentText())
        args.append(material)

        # 厚度参数
        thickness = self.thickness_edit.text()
        args.append(thickness)

        # 粒子类型
        particle = self.particle_combo.currentText()
        args.append(particle)

        # 能量参数
        energy = self.energy_edit.text()
        energy_unit = self.energy_unit_combo.currentText()
        args.append(f"{energy} {energy_unit}")

        # 清空输出
        self.output_text.clear()

        # 更新界面状态
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # 显示启动信息
        self.output_text.append("🚀 启动 Geant4量子 模拟...")
        self.output_text.append(f"📁 可执行文件: {exec_file}")
        self.output_text.append(f"⚙️ 模拟参数: {' '.join(args)}")
        self.output_text.append("-" * 60)

        # 启动模拟线程
        self.simulation_thread = SimulationThread(exec_file, args)
        self.simulation_thread.output_signal.connect(self.update_output)
        self.simulation_thread.finished_signal.connect(self.simulation_finished)
        self.simulation_thread.progress_signal.connect(self.update_progress)
        self.simulation_thread.start()

    def stop_simulation(self):
        """停止模拟"""
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.simulation_thread.stop()
            self.simulation_thread.terminate()
            self.simulation_thread.wait()
            self.output_text.append("⏹️ 模拟已停止")
            self.run_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.progress_bar.setVisible(False)

    def clear_output(self):
        """清空输出"""
        self.output_text.clear()

    def update_output(self, text):
        """更新输出显示"""
        self.output_text.append(text)
        # 自动滚动到底部
        scrollbar = self.output_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)

    def simulation_finished(self, exit_code):
        """模拟完成回调"""
        self.run_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)

        if exit_code == 0:
            self.output_text.append("-" * 60)
            self.output_text.append("✅ 模拟成功完成!")
        else:
            self.output_text.append("-" * 60)
            self.output_text.append(f"❌ 模拟异常结束，退出码: {exit_code}")


def main():
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle('Fusion')

    window = Geant4GUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()