from flask import request, jsonify, render_template, redirect, url_for, flash
from app import app
from services import auth_service


@app.post("/register")
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    existing_user = auth_service.get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "User already exists."}),  

    auth_service.register_user(email, password)
    return jsonify({"message": f"User {email} registered successfully."}), 201

@app.get("/users")
def get_users():
    users = auth_service.get_all_users()
    return jsonify([{"id": user.id, "email": user.email, "password":user.password} for user in users])

@app.get("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = auth_service.get_user_by_id(user_id)
    return jsonify({"id": user.id, "email": user.email,"password": user.password}), 200


@app.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = auth_service.get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.password != password:
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200
