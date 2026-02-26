from flask import Blueprint, render_template, request, redirect, url_for, flash

from database.models import Task
from database.engine import db

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
def get_all_tasks():
    try:
        show_only_incomplete = request.args.get('show_incomplete', False, type=bool)

        if show_only_incomplete:
            tasks = Task.query.filter_by(status='in_progress').all()
        else:
            tasks = Task.query.all()

        print(f"Found {len(tasks)} tasks")  # Отладка
        return render_template('index.html', tasks=tasks, show_only_incomplete=show_only_incomplete)
    except Exception as e:
        print(f"Error in get_all_tasks: {e}")
        return f"Error: {e}", 500


@tasks_bp.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            status = request.form.get('status', 'in_progress')
            task = Task(title=title, description=description, status=status)
            db.session.add(task)
            db.session.commit()
            flash('Task added!')
            return redirect(url_for('tasks.get_all_tasks'))
        except Exception as e:
            print(f"Error adding task: {e}")
            flash(f'Error: {e}')
            return redirect(url_for('tasks.get_all_tasks'))

    return render_template('add_task.html')

# Добавьте остальные маршруты...
