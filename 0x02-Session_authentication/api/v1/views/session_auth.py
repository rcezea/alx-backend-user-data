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
    """ Route for session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user:
        if user[0].is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            repr = user.to_json()
            name = os.getenv("SESSION_NAME")
            repr.set_cookie(name, session_id)
            return repr
        return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404
