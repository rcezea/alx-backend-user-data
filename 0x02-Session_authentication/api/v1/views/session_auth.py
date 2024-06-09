#!/usr/bin/env python3
""" Module of Session Auth views
"""
import os

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_login():
    """Authourise who to give access to
    resources"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user_obj = User.search({"email": email})
    if user_obj:
        if user_obj[0].is_valid_password(password):
            from api.v1.app import auth

            session_id = auth.create_session(user_obj[0].id)
            session_name = getenv("SESSION_NAME")
            resp = jsonify(user_obj[0].to_json())
            resp.set_cookie(session_name, session_id)
            return resp

        return jsonify({"error": "wrong password"}), 401

    return jsonify({"error": "no user found for this email"}), 404


@app_views.route(
    "/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Destroy the user session.
    """
    from api.v1.app import auth
    print('Here')
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
