from flask import request, jsonify, redirect, url_for
from app import app
from services import task_service
from models.task_model import Task
from datetime import datetime, timezone


@app.post("/tasks")
def create_task():
    data = request.get_json()
    content = data.get("content")
    due_date = datetime.strptime(data.get("due_date"), "%Y-%m-%d").replace(tzinfo=timezone.utc).date()
    if not content or not due_date:
        return jsonify({"error": "Missing content or deadline"}), 400
    task = task_service.create_task(content, due_date)
    return jsonify({"task": task.to_dict()}), 201

@app.get("/tasks")
def get_tasks():
    tasks = task_service.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks])


@app.get("/tasks/<int:task_id>")
def get_task_by_id(task_id):
    task = task_service.get_task_by_id(task_id)
    return jsonify(task.to_dict()), 200

@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json()
    task = task_service.get_task_by_id(task_id)
    content = data.get("content")
    due_date = datetime.strptime(data.get("due_date"), "%Y-%m-%d").replace(tzinfo=timezone.utc).date()
    task_service.update_task(task, content, due_date)
    return jsonify(task.to_dict())

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = task_service.get_task_by_id(task_id)
    task_service.delete_task(task)
    return jsonify({"message": "Task deleted"})

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    task = task_service.get_task_by_id(task_id)
    task_service.toggle_task_completion(task)
    return redirect(url_for("get_task_by_id", task_id=task_id))
