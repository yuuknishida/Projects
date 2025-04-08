from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sqlite3

PATH = '/Users/ynish/task-manager/data/tasks.db'

class Database():
    def __init__(self, parent=None):
        self.parent = parent

    '''CREATE DATABASE FOR THE APP IF DOESN'T EXISTS'''
    def setupDatabase(self):
        self.connection = sqlite3.connect(PATH)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            name TEXT, 
                            due_date TEXT, 
                            status TEXT, 
                            priority TEXT, 
                            created_date TEXT
                        )
                    ''')
        self.connection.commit()



    '''LOAD TASKS FROM DATABASE'''
    def fetchTasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        return tasks



    '''ADD TASKS TO DATABASE'''
    def insertTask(self, name, due_date_str, status, priority, created_date_str):
        self.cursor.execute("INSERT INTO tasks (name, due_date, status, priority, created_date) VALUES (?, ?, ?, ?, ?)", (name, due_date_str, status, priority, created_date_str))
        self.connection.commit()

    '''UPDATE DATABASE'''
    def updateTask(self, row, table):
        name_item = table.item(row, 0)
        due_date_item = table.item(row, 1)
        status_item = table.cellWidget(row, 2)
        status = status_item.currentText()

        if status == "Not Started":
            status_item.setStyleSheet("QComboBox {  background-color: lightgrey; border: none; border-radius: 10px;} QComboBox::drop-down {border: none;} QComboBox::down-arrow { image: none; } ")        
        elif status == "In Progress":
            status_item.setStyleSheet("QComboBox {  background-color: lightblue; border: none; border-radius: 10px;} QComboBox::drop-down {border: none;} QComboBox::down-arrow { image: none; } ")        
        elif status == "Completed":
            status_item.setStyleSheet("QComboBox {  background-color: lightgreen; border: none; border-radius: 10px;} QComboBox::drop-down {border: none;} QComboBox::down-arrow { image: none; } ")

        priority_item = table.cellWidget(row, 3)
        priority = priority_item.currentText()

        if priority == "High":
            priority_item.setStyleSheet("QComboBox {  background-color: red; border: none; border-radius: 10px;} QComboBox::drop-down {border: none; } QComboBox::down-arrow { image: none; }") 
        elif priority == "Medium":
            priority_item.setStyleSheet("QComboBox {  background-color: yellow; border: none; border-radius: 10px;} QComboBox::drop-down {border: none; } QComboBox::down-arrow { image: none; }") 
        elif priority == "Low":
            priority_item.setStyleSheet("QComboBox { background-color: green; border: none; border-radius: 10px;} QComboBox::drop-down {border: none; } QComboBox::down-arrow { image: none;}") 

        name = name_item.text()
        due_date_str = QDateTime.fromString(due_date_item.text(), "dddd, dd MMMM yyyy h:mm AP").toString(Qt.ISODate)
        status = status_item.currentText()
        priority = priority_item.currentText()
        self.cursor.execute("UPDATE tasks SET due_date=?, status = ?, priority = ? WHERE name = ?", (due_date_str, status, priority, name))
        self.connection.commit()
    
    def deleteTask(self, row, table):
        name = table.item(row, 0).text()
        self.cursor.execute("DELETE FROM tasks WHERE name = ?", (name,))
        self.connection.commit()
