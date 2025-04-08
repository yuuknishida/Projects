from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from datetime import datetime
from jinja2 import Template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

db.init_app(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime(), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Not Started')
    created = db.Column(db.DateTime(), nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, task_name, due_date, priority, status, created):
        self.task_name = task_name
        self.due_date = due_date
        self.priority = priority
        self.created = created
        self.progress = 0
        self.status = status

    def __repr__(self):
        return f'<Task {self.id} - {self.task_name}>'
    
def update_progress(due_date, created):
    now = datetime.now()
    if now >= due_date:
        return 100
    else:
        total_time = (due_date - created)
        elapsed_time = (now - created)
        return int((elapsed_time / total_time) * 100)
    print("total time:", total_time, "elapsed time:", elapsed_time)
        
@app.route('/', methods=['GET', 'POST'])
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks, update_progress=update_progress)

def is_task_exist(task_name):
    task_name_exists = db.session.query(exists().where(Task.task_name == task_name)).scalar()
    return task_name_exists

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        # Gets data from request add-task.html
        task_name = request.form['taskName']
        combined_due_date = request.form['combinedDateTime']

        # Sets up due date
        due_date = datetime.strptime(combined_due_date, '%Y-%m-%d %H:%M')
        
        priority = request.form['taskPriority']
        current_date = datetime.now()

        # Checks if any of these fields are empty
        if task_name == '' or combined_due_date == '' or priority == '':
            return render_template('add_task.html', error='Please fill in all fields')
        
        # Checks if the task name exists
        if is_task_exist(task_name):
            flash(f"Task {task_name} already exists")
            return redirect(url_for("add_task"))
        
        new_task = Task(task_name=task_name, due_date=due_date, priority=priority, status="Not Started", created=current_date)
        new_task.update_progress()
        db.session.add(new_task)
        db.session.commit()
        flash(f"Task {task_name} added successfully")
        return redirect(url_for("home"))
    
    return render_template('add_task.html')

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get(task_id)
    
    if 'priority' in request.form:
        task.priority = request.form.get('priority')
    elif 'status' in request.form:
        task.status = request.form.get('status')

    task.update_progress()

    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete_task/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    if request.method == 'POST':
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            flash(f"Task {task.task_name} deleted successfully")
        else:
            flash("Task not found")
        return redirect(url_for('home'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)