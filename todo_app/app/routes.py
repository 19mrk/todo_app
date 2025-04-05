from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import Task
from . import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    sort_by = request.args.get('sort_by', 'due_date')
    tasks = Task.query.order_by(getattr(Task, sort_by).asc()).all()
    return render_template('index.html', tasks=tasks)

@main.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
    priority = request.form['priority']
    category = request.form['category']

    new_task = Task(title=title, description=description, due_date=due_date,
                    priority=priority, category=category)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/toggle/<int:task_id>')
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/calendar')
def calendar_view():
    return render_template('calendar.html')

@main.route('/api/tasks')
def get_tasks_json():
    tasks = Task.query.all()
    events = [{
        'title': task.title,
        'start': task.due_date.strftime('%Y-%m-%d'),
        'url': url_for('main.index')
    } for task in tasks]
    return jsonify(events)

