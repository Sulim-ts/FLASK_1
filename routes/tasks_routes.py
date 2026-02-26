from flask import Blueprint, render_template, request, redirect, url_for, flash

from database.models import Task
from database.engine import db

# Создаем сам Blueprint
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def get_all_tasks():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@tasks_bp.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        flash('Task added!')
        return redirect(url_for('tasks.get_all_tasks'))

    return render_template('add_task.html')

@tasks_bp.route('/<int:task_id>')
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!')
    return redirect(url_for('tasks.get_all_tasks'))