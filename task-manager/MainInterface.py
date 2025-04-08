import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QSpacerItem, QGridLayout, QSizePolicy, QStackedWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QProgressBar, QHeaderView, QLineEdit, QDateTimeEdit, QComboBox, QDialog, QLabel, QFormLayout, QDialogButtonBox, QHBoxLayout, QMessageBox, QFrame
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QRect
from PyQt5.QtGui import QFont, QIcon, QPixmap

DASHBOARD = "icons/dashboards.png"
MENU = "icons/menu.png"
PLUS = "icons/plus.png"
LOGO = "icons/task-management-icon-29.jpg"

class PageWindow(QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)

class MainInterface(PageWindow):
    def __init__(self):
        super().__init__()
        self.isSidebarVisible = True
        self.setWindowTitle("Task Manager")
        self.setWindowIcon(QIcon(LOGO))
        self.setGeometry(100, 100, 800, 800)
        self.initUI()

    def initUI(self):
        '''CENTRAL WIDGET '''
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        '''SIDEBAR '''
        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: rgb(0, 170, 255); border-radius: 10px;")
        self.sidebar.setFixedWidth(250)

        '''SIDEBAR LAYOUT '''
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setSpacing(20)
        self.sidebar_layout.setContentsMargins(0,0,0,0)

        '''SIDEBAR HEADER '''
        self.header_icon = QLabel()
        logo = QPixmap(LOGO)
        self.header_icon.setPixmap(logo)
        self.header_icon.setScaledContents(True)
        self.header_icon.setFixedSize(60, 60)

        self.header = QLabel("Task Manager")
        self.header.setFont(QFont('Arial', 14))
        self.header.setStyleSheet("""color: white: font-size: 18px; font-weight: bold;""")
        self.header.setAlignment(Qt.AlignVCenter)

        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(10, 10, 10, 10)
        self.header_layout.addWidget(self.header_icon)
        self.header_layout.addWidget(self.header)
        
        self.sidebar_layout.addLayout(self.header_layout)

        '''SPACR ITEM BELOW HEADER'''
        spacer1 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidebar_layout.addItem(spacer1)

        '''SIDEBAR BTNS '''
        self.dashboard_label = self.createSidebarButton("Dashboard", DASHBOARD)
        self.btn.clicked.connect(self.createPageSwitchHandler("dashboard"))
        
        self.add_task_label = self.createSidebarButton("Add Task", PLUS)
        self.btn.clicked.connect(self.createPageSwitchHandler("add tasks"))
        
        '''SPACER ITEM BETWEEN BUTTONS AND BOTTOM'''
        spacer2 = QSpacerItem(20, 1000, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidebar_layout.addItem(spacer2)

        '''SIDEBAR TOGGLE BTN '''
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(QIcon(MENU))
        self.toggle_btn.setFixedSize(40, 40)
        self.toggle_btn.setIconSize(QSize(32,32))
        self.toggle_btn.setStyleSheet("""QPushButton:hover {background-color: #a5a5a5;} QPushButton {color: white; background-color: rgb(0, 170, 255); border: none; font-size: 16px; border-radius: 10px;}""")
        self.toggle_btn.clicked.connect(self.toggleSidebarDisplay)

        '''MAIN LAYOUT '''
        self.main_layout = QHBoxLayout(self.central_widget)
        toggle_btn_layout = QVBoxLayout()
        toggle_btn_layout.addWidget(self.toggle_btn)
        toggle_btn_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addLayout(toggle_btn_layout)

        '''CREATE THE MAIN CONTENT AREA'''
        content_area = QWidget(self)
        content_area.setStyleSheet("""background-color: #ecf0f1;""")
        self.main_layout.addWidget(content_area)
    
    '''METHOD TO TOGGLE THE SIDEBAR'''
    def toggleSidebarDisplay(self):
        if self.isSidebarVisible:
            self.sidebar.setFixedWidth(80)
            self.header.setVisible(False)
            self.dashboard_label.setVisible(False)
            self.add_task_label.setVisible(False)
        else:
            self.sidebar.setFixedWidth(250)
            self.header.setVisible(True)
            self.dashboard_label.setVisible(True)
            self.add_task_label.setVisible(True)

        self.isSidebarVisible = not self.isSidebarVisible

    '''METHOD TO ADD A SIDEBAR BTN '''
    def createSidebarButton(self, name, icon_path):
        self.btn = QPushButton()
        self.btn.setIcon(QIcon(icon_path))
        self.btn.setFixedSize(60, 60)
        self.btn.setIconSize(QSize(32,32))
        self.btn.setStyleSheet("""QPushButton:hover {background-color: #1abc9c;} QPushButton {color: white; background-color: rgb(0, 170, 255); border: none; font-size: 16px;}""")
        self.btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        name_label = QLabel(name)
        name_label.setStyleSheet("""padding-left: 10px;""")
        name_label.setFont(QFont('Arial', 14))
        name_label.setAlignment(Qt.AlignVCenter)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn)
        btn_layout.addWidget(name_label)
        btn_layout.addStretch()

        btn_widget = QWidget()
        btn_widget.setLayout(btn_layout)
        self.sidebar_layout.addWidget(btn_widget)

        return name_label
    
    def createPageSwitchHandler(self, page_name):
        def handleButton():
            self.goto(page_name)
        return handleButton