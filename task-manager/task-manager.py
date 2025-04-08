import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy, QStackedWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QProgressBar, QHeaderView, QLineEdit, QDateTimeEdit, QComboBox, QDialog, QLabel, QFormLayout, QDialogButtonBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon
import sqlite3


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 1000, 800)
        self.sidebar_expanded = True
        self.initUI()
        self.create_db()
        self.load_tasks_from_db()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        # Sidebar layout
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(50)
        self.sidebar_layout.setObjectName("sidebar_layout")

        # Sidebar label
        self.sidebar_label_layout = QVBoxLayout()
        self.sidebar_label_layout.setAlignment(Qt.AlignTop)
        self.sidebar_label_layout.setSpacing(50)

        # Expand/Collapse Button
        self.expand_button = QPushButton()
        self.expand_button.setToolTip("Expand Sidebar")
        self.expand_button.setIcon(QIcon("icons/menu-burger.png"))
        self.expand_button.setFixedSize(40,40)
        self.expand_button.setIconSize(QSize(32,32))
        self.expand_button.setFont(QFont('Arial', 12))
        self.expand_button.clicked.connect(self.toggle_sidebar)

        expand_layout = QHBoxLayout()
        expand_layout.addWidget(self.expand_button)
        expand_layout.addStretch()
        

        expand_widget = QWidget()
        expand_widget.setLayout(expand_layout)
        expand_widget.setStyleSheet("background-color: #4CAF50;")
        self.sidebar_layout.addWidget(expand_widget)

        # Add Task Button and label
        self.add_task_button = QPushButton()
        self.add_task_button.setToolTip("Add Task")
        self.add_task_button.setIcon(QIcon("icons/plus.png"))
        self.add_task_button.setFixedSize(40, 40)
        self.add_task_button.setIconSize(QSize(32,32))
        self.add_task_button.setFont(QFont('Arial', 12))
        self.add_task_button.clicked.connect(self.open_add_task_dialog)

        self.add_task_button_label = QLabel("Add Task")
        self.add_task_button_label.setAlignment(Qt.AlignCenter)
        self.add_task_button_label.hide()

        add_task_layout = QHBoxLayout()
        add_task_layout.addWidget(self.add_task_button)
        add_task_layout.addWidget(self.add_task_button_label)
        add_task_layout.addStretch()

        add_task_widget = QWidget()
        add_task_widget.setLayout(add_task_layout)
        add_task_widget.setStyleSheet("background-color: #4CAF50;")
        self.sidebar_layout.addWidget(add_task_widget)

        # Home Page Button
        self.home_button = QPushButton()
        self.home_button_label = QLabel("Home")
        self.home_button_label.setAlignment(Qt.AlignTop)
        self.home_button_label.hide()
        self.home_button.setToolTip("Home")
        self.home_button.setIcon(QIcon("icons/home.png"))
        self.home_button.setFixedSize(40, 40)
        self.home_button.setIconSize(QSize(32,32))
        self.home_button.setFont(QFont('Arial', 12))
        self.home_button.clicked.connect(self.show_home_page)

        self.home_button_label = QLabel("Home")
        self.home_button_label.setAlignment(Qt.AlignCenter)
        self.home_button_label.hide()

        home_layout = QHBoxLayout()
        home_layout.addWidget(self.home_button)
        home_layout.addWidget(self.home_button_label)
        home_layout.addStretch()

        home_widget = QWidget()
        home_widget.setLayout(home_layout)
        home_widget.setStyleSheet("background-color: #4CAF50;")
        self.sidebar_layout.addWidget(home_widget)
        

        # Tasks View Button
        self.tasks_button = QPushButton()
        self.tasks_button.setToolTip("View Tasks")
        self.tasks_button.setIcon(QIcon("icons/checklist.png"))
        self.tasks_button.setFixedSize(40, 40)
        self.tasks_button.setIconSize(QSize(32,32))
        self.tasks_button.setFont(QFont('Arial', 12))
        self.tasks_button.clicked.connect(self.show_tasks_view)

        self.tasks_button_label = QLabel("View Tasks")
        self.tasks_button_label.setAlignment(Qt.AlignCenter)
        self.tasks_button_label.hide()

        tasks_layout = QHBoxLayout()
        tasks_layout.addWidget(self.tasks_button)
        tasks_layout.addWidget(self.tasks_button_label)
        tasks_layout.addStretch()

        tasks_widget = QWidget()
        tasks_widget.setLayout(tasks_layout)
        tasks_widget.setStyleSheet("background-color: #4CAF50;")
        self.sidebar_layout.addWidget(tasks_widget)

        # Sidebar Container
        self.sidebar_container = QWidget()
        self.sidebar_container.setLayout(self.sidebar_layout)
        self.sidebar_container.setFixedWidth(80)
        self.sidebar_container.setObjectName("sidebar_container")

        # Stacked widget to hold different views
        self.stacked_widget = QStackedWidget()

        # Home Page
        self.home_page = QWidget()
        self.home_page_layout = QVBoxLayout()
        self.home_page_label = QLabel("Statistics will be shown here.")
        self.home_page_layout.addWidget(self.home_page_label)
        self.home_page.setLayout(self.home_page_layout)

        # Tasks View (Table)
        self.tasks_view = QWidget()
        tasks_view_layout = QVBoxLayout()
        tasks_view_layout.addSpacing(20)
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["Name", "Due Date", "Status", "Priority", "Created Date", "Progress", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        tasks_view_layout.addWidget(self.table)
        self.tasks_view.setLayout(tasks_view_layout)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.tasks_view)

        # Add widgets to the main layout
        main_layout.addWidget(self.sidebar_container)
        main_layout.addWidget(self.stacked_widget)

        # Conainer widget to the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Timer for progress update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rows)
        self.timer.start(60000)

        # apply custom styles
        self.setStyleSheet(self.load_styles())

    def create_db(self):
        try:
            self.conn = sqlite3.connect('tasks.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (name TEXT, due_date TEXT, status TEXT, priority TEXT, created_date TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while creating the database: {e}")

    def load_tasks_from_db(self):
        try:
            self.cursor.execute("SELECT * FROM tasks")
            tasks = self.cursor.fetchall()
            for task in tasks:
                self.add_task_to_table(*task)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while loading tasks from the database: {e}")

    def add_task_to_db(self, name, due_date_str, status, priority, created_date_str):
        try:
            self.cursor.execute("INSERT INTO tasks (name, due_date, status, priority, created_date) VALUES (?, ?, ?, ?, ?)", (name, due_date_str, status, priority, created_date_str))
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while adding task to the database: {e}")

    def open_add_task_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Task")
        dialog_layout = QFormLayout(dialog)

        name_input = QLineEdit()
        due_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        due_date_input.setCalendarPopup(True)
        due_date_input.setDisplayFormat("dddd, dd MMMM yyyy h:mm AP")
        status_input = QComboBox()
        status_input.addItems(["Not Started", "In Progress", "Completed"])
        priority_input = QComboBox()
        priority_input.addItems(["High", "Medium", "Low"])
        created_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        created_date_input.setCalendarPopup(True)
        created_date_input.setDisplayFormat("dddd, dd MMMM yyyy h:mm AP")

        dialog_layout.addRow("Name:", name_input)
        dialog_layout.addRow("Due Date:", due_date_input)
        dialog_layout.addRow("Status:", status_input)
        dialog_layout.addRow("Priority:", priority_input)
        dialog_layout.addRow("Created Date:", created_date_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)

        if dialog.exec() == QDialog.Accepted:
            name = name_input.text()
            due_date_str = due_date_input.dateTime().toString(Qt.ISODate)
            status = status_input.currentText()
            priority = priority_input.currentText()
            created_date_str = created_date_input.dateTime().toString(Qt.ISODate)
            self.add_task_to_table(name, due_date_str, status, priority, created_date_str)
            self.add_task_to_db(name, due_date_str, status, priority, created_date_str)

    def add_task_to_table(self, name, due_date_str, status, priority, created_date_str):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        name_item = QTableWidgetItem(name)
        name_item.setToolTip(name)
        due_date = QDateTime.fromString(due_date_str, Qt.ISODate)
        due_date_item = QTableWidgetItem(due_date.toString("dddd, dd MMMM yyyy h:mm AP"))
        due_date_tooltip = due_date.toString("dddd, dd MMMM yyyy h:mm AP")
        due_date_item.setToolTip(due_date_tooltip)

        status_item = QComboBox()
        status_item.setFixedSize(120, 40)
        status_item.addItems(["Not Started", "In Progress", "Completed"])
        status_item.setCurrentText(status)
        status_item.currentIndexChanged.connect(lambda: self.update_task_in_db(row_position))
        self.apply_status_style(status_item, status)

        priority_item = QComboBox()
        priority_item.setFixedSize(90, 40)
        priority_item.addItems(["High", "Medium", "Low"])
        priority_item.setCurrentText(priority)
        priority_item.currentIndexChanged.connect(lambda: self.update_task_in_db(row_position))
        self.apply_priority_style(priority_item, priority)

        created_date = QDateTime.fromString(created_date_str, Qt.ISODate)
        created_date_item = QTableWidgetItem(created_date.toString("dddd, dd MMMM yyyy h:mm AP"))
        created_date_tooltip = created_date.toString("dddd, dd MMMM yyyy h:mm AP")
        created_date_item.setToolTip(created_date_tooltip)

        progress_bar = QProgressBar()
        progress_bar.setAlignment(Qt.AlignCenter)

        # Center text in the cells
        for item in [due_date_item, created_date_item]:
            item.setTextAlignment(Qt.AlignCenter)

        # Delete Button
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("background-color: red; color: white;")
        delete_button.clicked.connect(lambda: self.delete_task(row_position))

        self.table.setItem(row_position, 0, name_item)
        self.table.setItem(row_position, 1, due_date_item)
        self.table.setCellWidget(row_position, 2, status_item)
        self.table.setCellWidget(row_position, 3, priority_item)
        self.table.setItem(row_position, 4, created_date_item)
        self.table.setCellWidget(row_position, 5, progress_bar)
        self.table.setCellWidget(row_position, 6, delete_button)

        self.update_progress_bar(progress_bar, due_date, created_date)

    def update_task_in_db(self, row):
        name_item = self.table.item(row, 0)
        due_date_item = self.table.item(row, 1)
        status_item = self.table.cellWidget(row, 2)
        priority_item = self.table.cellWidget(row, 3)
        name = name_item.text()
        due_date_str = QDateTime.fromString(due_date_item.text(), "dddd, dd MMMM yyyy h:mm AP").toString(Qt.ISODate)
        status = status_item.currentText()
        priority = priority_item.currentText()
        try:
            self.cursor.execute("UPDATE tasks SET due_date=?, status = ?, priority = ? WHERE name = ?", (due_date_str, status, priority, name))
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while updating task in the database: {e}")

        self.apply_status_style(self.table.cellWidget(row, 2), status)
        self.apply_priority_style(self.table.cellWidget(row, 3), priority)

    def delete_task(self, row):
        confirm = QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?", QMessageBox.Yes | QMessageBox.No)    
        if confirm == QMessageBox.Yes:
            try:
                name = self.table.item(row, 0).text()
                self.cursor.execute("DELETE FROM tasks WHERE name = ?", (name,))
                self.conn.commit()
                self.table.removeRow(row)
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"An error occurred while deleting task from the database: {e}")

    def update_progress_bar(self, progress_bar, due_date, created_date):
        now = QDateTime.currentDateTime()
        if due_date > now:
            total_time = due_date.toSecsSinceEpoch() - created_date.toSecsSinceEpoch()
            elapsed_time = now.toSecsSinceEpoch() - created_date.toSecsSinceEpoch()
            progress = int((elapsed_time / total_time) * 100)

            progress_bar.setValue(progress)
            if progress < 33:
                progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; border-radius: 10px;}")
            elif progress < 66:
                progress_bar.setStyleSheet("QProgressBar::chunk { background-color: yellow; border-radius: 10px;}")
            else:
                progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; border-radius: 10px;}")
            progress_bar.setFormat("%p%")
        else:
            progress_bar.setValue(100)
            progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; border-radius: 10px;}")
            progress_bar.setFormat("Deadline Reached")

    def update_rows(self):
        row_count = self.table.rowCount()
        for row in range(row_count):
            created_date_str = self.table.item(row, 4).text()
            created_date = QDateTime.fromString(created_date_str, "dddd, dd MMMM yyyy h:mm AP")
            due_date_str = self.table.item(row, 1).text()
            due_date = QDateTime.fromString(due_date_str, "dddd, dd MMMM yyyy h:mm AP")
            progress_bar = self.table.cellWidget(row, 5)
            self.update_progress_bar(progress_bar, due_date, created_date)

    def apply_status_style(self, status_item, status):
        if status == "Not Started":
            status_item.setStyleSheet("QComboBox { background-color: lightgrey; border: none; border-radius: 10px;} QComboBox::drop-down {border: none;} QComboBox::down-arrow { image: none; } ")        
        elif status == "In Progress":
            status_item.setStyleSheet("QComboBox { background-color: lightblue; border: none; border-radius: 10px;} QComboBox::drop-down {border: none;} QComboBox::down-arrow { image: none; } ")        
        elif status == "Completed":
            status_item.setStyleSheet("QComboBox { background-color: lightgreen; border: none; border-radius: 10px;} QComboBox::drop-down {border: none;} QComboBox::down-arrow { image: none; } ")        
        

    def apply_priority_style(self, priority_item, priority):
        if priority == "High":
            priority_item.setStyleSheet("QComboBox { margin-left: 5px; background-color: red; border: none; border-radius: 10px;} QComboBox::drop-down {border: none; } QComboBox::down-arrow { image: none; }") 
        elif priority == "Medium":
            priority_item.setStyleSheet("QComboBox { margin-left: 5px; background-color: yellow; border: none; border-radius: 10px;} QComboBox::drop-down {border: none; } QComboBox::down-arrow { image: none; }") 
        elif priority == "Low":
            priority_item.setStyleSheet("QComboBox { margin-left: 5px; background-color: green; border: none; border-radius: 10px;} QComboBox::drop-down {border: none; } QComboBox::down-arrow { image: none;}") 

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_tasks_view(self):
        self.stacked_widget.setCurrentWidget(self.tasks_view)

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar_container.setFixedWidth(200)
            self.expand_button.setToolTip("Expand Sidebar")
            self.expand_button.setIcon(QIcon("icons/collapse.png"))
            self.update_sidebar_labels()
        else:
            self.sidebar_container.setFixedWidth(80)
            self.expand_button.setToolTip("Collapse Sidebar")
            self.expand_button.setIcon(QIcon("icons/menu-burger.png"))
            self.clear_sidebar_labels()

        self.sidebar_expanded = not self.sidebar_expanded

    def update_sidebar_labels(self):
        self.add_sidebar_label()

    def clear_sidebar_labels(self):
        self.remove_sidebar_label()

    def add_sidebar_label(self):
        self.add_task_button_label.show()
        self.home_button_label.show()
        self.tasks_button_label.show()

    def remove_sidebar_label(self):
        self.add_task_button_label.hide()
        self.home_button_label.hide()
        self.tasks_button_label.hide()

    def load_styles(self):
        return """
        QMainWindow {
            background-color: #F5F5F5;
        }
        QWidget {
            background-color: #ECEFF4;
            color: #2E3440;
            font-size: 18px;
        }
        QTableWidget {
            background-color: #F9F9F9;
            alternate-background-color: #E0F7FA;
            selection-background-color: #00ACC1;
            color: #2E3440;
            border: 1px solid #DDDDDD;
            gridline-color: #4C566A;
        }
        QHeaderView::section {
            background-color: #DDDDDD;
            padding: 5px;
            border: none;
            font-weight: bold;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QLabel {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 5px;
            margin-left: 0px;
        }
        QPushButton:hover {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
        }
        QDialog {
            background-color: #ECEFF4;
            color: #2E3440;
            font-size: 16px;
        }
        QComboBox {
            background-color: #3B4252;
            color: #2E3440;
            border: 1px solid #4C566A;
            border-radius: 12px;
            padding: 5px;
        }
        QComboBox QAbstractItemView {
            background-color: #ECEFF4;
            color: #2E3440;
            selection-background-color: #5E81AC;
            selection-color: #ECEFF4;
            text-align: center;
            }
        QDialogButtonBox QPushButton {
            background-color: #5E81AC;
            color: #ECEFF4;
            border: none;
            padding: 5px;
            border-radius: 5px;
        }
        QDialogButtonBox QPushButton:hover {
            background-color: #81A1C1;
        }
        QProgressBar {
            border: 1px solid #555;
            text-align: center;
            border-radius: 10px;
        }
        QProgressBar::chunk {
        }
        #sidebar_container {
            background-color: #4CAF50;
        }
        #sidebar_layout {
            background-color: #4CAF50;
        }
        QLineEdit {
            border: 1px solid #4C566A;
            border-radius: 10px;
            padding: 5px;
            background-color: #E5E9F0;
            color: #2E3440;
        }
        """

def main():
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()