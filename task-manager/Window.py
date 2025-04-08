from PyQt5 import QtCore, QtWidgets, QtGui
from Pages import *

class AppMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.database = Database()
        self.database.setupDatabase()

        self.dashboard = DashboardPage(self.database)
        self.addTaskPage = AddTaskPage(self.database, self.dashboard)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.n_pages = {}

        self.register(self.addTaskPage, "add tasks")
        self.register(self.dashboard, "dashboard")

        self.navigateTo("dashboard")

    def register(self, widget, name):
        self.n_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.navigateTo)

    @QtCore.pyqtSlot(str)
    def navigateTo(self, name):
        if name in self.n_pages:
            widget = self.n_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())