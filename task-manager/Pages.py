from MainInterface import *
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QColor, QPalette
from Database import Database
from MainInterface import MainInterface


class AddTaskPage(MainInterface):
    def __init__(self, database, dashboard):
        super().__init__()
        self.database = database
        self.dashboard = dashboard
        self.initUi()

    def initUi(self):
        self.setWindowTitle('Add Task')
        self.create_form_layout()

    def create_form_layout(self):
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(20)

        status_combo = QComboBox()
        priority_combo = QComboBox()
        status_combo.addItems(["Not Started", "In Progress", "Completed"])
        priority_combo.addItems(["High", "Medium", "Low"])


        self.add_form_row("Name: ", QLineEdit(), self.form_layout)
        self.add_form_row("Due Date: ", QDateTimeEdit(QDateTime.currentDateTime(), calendarPopup=True, displayFormat="dddd, dd MMMM yyyy h:mm AP"), self.form_layout)
        self.add_form_row("Status: ", status_combo, self.form_layout)
        self.add_form_row("Priority: ", priority_combo, self.form_layout)
        self.add_form_row("Created Date: ", QDateTimeEdit(QDateTime.currentDateTime(), calendarPopup=True, displayFormat="dddd, dd MMMM yyyy h:mm AP"), self.form_layout)

        self.save_btn = QPushButton("Save", clicked=self.saveTask)
        self.save_btn.setFixedSize(40, 40)
        self.form_layout.addWidget(self.save_btn)

        self.main_layout.addLayout(self.form_layout, stretch=1)

    def add_form_row(self, label_text, widget, layout):
        label = QLabel(label_text)
        label.setFont(QFont('Arial', 14))
        widget.setFont(QFont('Arial', 14))
        widget.setFixedSize(500, 50)

        row_layout = QHBoxLayout()
        row_layout.addWidget(label)
        row_layout.addWidget(widget)
        row_layout.addStretch(1)

        layout.addLayout(row_layout)

    def saveTask(self):
        name = self.name_input.text()
        if not name:
            QMessageBox.critical(self, "Error", "Please enter a task name.")
            return
        
        due_date_str = self.due_date_input.dateTime().toString(Qt.ISODate)
        status = self.status_input.currentText()
        priority = self.priority_input.currentText()
        created_date_str = self.created_date_input.dateTime().toString(Qt.ISODate)

        response = self.confirm_task_details(name, due_date_str, status, priority, created_date_str)
        if response == QMessageBox.Yes:
            self.databasae.insertTask(name, due_date_str, status, priority, created_date_str)
            self.dashboard.addTaskToTable(name, due_date_str, status, priority, created_date_str)
            QMessageBox.information(self, "Success", "Task saved successfully!")
            self.clear_form()
            self.goto("dashboard")

    def confirm_task_details(self, name, due_date_str, status, priority, created_date_str):
        msg_box = QMessageBox(QMessageBox.Question, "Confirm Task", f"Name: {name}\nDue Date: {due_date_str}\nStatus: {status}\nPriority: {priority}\nCreated Date: {created_date_str}")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg_box.exec_()
    
    def clear_form(self):
        self.name_input.clear()
        self.due_date_input.clear()
        self.status_input.setCurrentIndex(0)
        self.priority_input.setCurrentIndex(0)
        self.created_date_input.clear()



class DashboardPage(MainInterface):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.initUi()
    
    def initUi(self):
        self.setWindowTitle('Dashboard')
        self.setStyleSheet(self.setTableStyle())
        self.create_table()
        

    def create_table(self):
        tasks = self.database.fetchTasks()
        
        self.table = QTableWidget(columnCount=7)
        self.table.setHorizontalHeaderLabels(["Name", "Due Date", "Status", "Priority", "Created Date", "Progress", "Action"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        for task in tasks:
            self.addTaskToTable(*task)

        self.main_layout.addWidget(self.table)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_bar)
        self.timer.start(60000)

    def addTaskToTable(self, name, due_date_str, status, priority, created_date_str):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, self.create_table_item(name))
        self.table.setItem(row, 1, self.create_date_item(due_date_str))
        self.table.setCellWidget(row, 2, self.create_combo_box(["Not Started", "In Progress", "Completed"], status, row))
        self.table.setCellWidget(row, 3, self.create_combo_box(["High", "Medium", "Low"], priority, row))
        self.table.setItem(row, 4, self.create_date_item(created_date_str))

        self.add_progress_bar(row, due_date_str, created_date_str)
        self.add_delete_button(row)

    def create_table_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item
    
    def create_date_item(self, date_str):
        date = QDateTime.fromString(date_str, Qt.ISODate)
        date_text = date.toString("dddd, dd MMMM yyyy h:mm AP")
        return self.create_table_item(date_text)
    
    def create_combo_box(self, items, current_text, row):
        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.setCurrentText(current_text)
        combo_box.currentTextChanged.connect(lambda: self.update_combo_box_color(combo_box, combo_box.currentText()))
        self.update_combo_box_color(combo_box, current_text)
        combo_box.currentIndexChanged.connect(lambda: self.database.updateTask(row, self.table))
        return combo_box
    
    def update_combo_box_color(self, combo_box, selected_option):
        color_dict = {
            "High": "red",    
            "Medium": "orange", 
            "Low": "green",      
            "Completed": "lightgreen",
            "In Progress": "lightblue",
            "Not Started": "lightgrey" 
        }

        color = color_dict.get(selected_option)
        combo_box.setStyleSheet(f"QComboBox {{ background-color: {color}}}")
    
    def add_progress_bar(self, row, due_date_str, created_date_str):
        bar = QProgressBar()
        bar.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, 5, bar)
        self.calculate_progress(bar, due_date_str, created_date_str)

    def update_bar(self):
        for row in range(self.table.rowCount()):
            created_date_str = self.table.item(row, 4).toolTip()
            due_date_str = self.table.item(row, 1).toolTip()
            progress_bar = self.table.cellWidget(row, 5)
            self.calculate_progress(progress_bar, due_date_str, created_date_str)

    def calculate_progress(self, bar, due_date_str, created_date_str):
        now = QDateTime.currentDateTime() 
        created_date = QDateTime.fromString(created_date_str, Qt.ISODate)
        due_date = QDateTime.fromString(due_date_str, Qt.ISODate)

        if due_date > now:  
            total_time = due_date.toSecsSinceEpoch() - created_date.toSecsSinceEpoch()
            elapsed_time = now.toSecsSinceEpoch() - created_date.toSecsSinceEpoch()

            progress = int((elapsed_time / total_time) * 100)
            bar.setValue(progress)
            bar.setStyleSheet(self.get_progress_bar_color(progress))
    
    def get_progress_bar_color(self, progress):
        if progress < 33:
            return "QProgressBar::chunk { background-color: green; }"
        elif progress < 66:
            return "QProgressBar::chunk { background-color: yellow; }"
        else:
            return "QProgressBar::chunk { background-color: red; }"  

    def add_delete_button(self, row):
        delete_button = QPushButton("Delete")         
        delete_button.setStyleSheet("background-color: red; color: white")
        delete_button.clicked.connect(lambda: self.delete_Task(row))
        self.table.setCellWidget(row, 6, delete_button)
   
        
    def delete_Task(self, row):
        confirm = QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?", QMessageBox.Yes | QMessageBox.No)    
        if confirm == QMessageBox.Yes:
            try:
                self.database.deleteTask(row, self.table)
                self.table.removeRow(row)
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"An error occurred while deleting task from the database: {e}")

    def setTableStyle(self):
        return """
        QTableWidget {
            background-color: #F9F9F9;
            alternate-background-color: #E0F7FA;
            selection-background-color: #00ACC1;
            color: #2E3440;
            border: 1px solid #DDDDDD;
            gridline-color: #4C566A;
            text-align: center;
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

        QComboBox {
            border-radius: 10px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            image: none;
        }
        """