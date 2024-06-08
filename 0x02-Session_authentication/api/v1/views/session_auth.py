#!/usr/bin/env python3
""" Module of Session Auth views
"""
import os

from api.v1.views import app_views
from flask import abort, jsonify, request
from api.v1.auth.session_auth import SessionAuth
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_session():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user) <= 0:
        return None
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        auth.create_session(user.id)
        repr = user.to_json()
        name = os.getenv("SESSION_NAME")
        out.set_cookie(name, repr)
        return out
