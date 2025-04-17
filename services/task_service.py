from models.task_model import Task
from app import db
from datetime import datetime

def create_task(content, due_date):
    days_remaining = (due_date - datetime.today().date()).days
    new_task = Task(content=content, due_date=due_date, days_remaining=days_remaining)
    db.session.add(new_task)
    db.session.commit()
    return new_task

def get_all_tasks():
    return Task.query.order_by(Task.date_created).all()

def get_task_by_id(task_id):
    return Task.query.get_or_404(task_id)

def update_task(task, content, due_date):
    task.content = content
    task.due_date = due_date
    task.days_remaining = (due_date - datetime.today().date()).days
    db.session.commit()
    return task

def delete_task(task):
    db.session.delete(task)
    db.session.commit()

def toggle_task_completion(task):
    task.is_completed = not task.is_completed
    db.session.commit()
    return task