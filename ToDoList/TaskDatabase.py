import sqlite3

class TaskDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('tasks.db')
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT, 
                priority TEXT,
                status TEXT,
                due_date TEXT
            )
        ''')
        self.connection.commit()

    def add_task(self, name, description, priority, status, due_date):
        self.cursor.execute("INSERT INTO tasks (id, name, description, priority, status, due_date) VALUES (?, ?, ?, ?, ?, ?)", (name, description, priority, status, due_date))

    def remove_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        pass

    def update_task(self, task_id, name, description, priority, status, due_date):
        self.cursor.execute("UPDATE tasks SET name = ?, description = ?, priority = ?, status = ?, due_date = ? WHERE id = ?", (task_id, name, description, priority, status, due_date))

    def get_all_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()