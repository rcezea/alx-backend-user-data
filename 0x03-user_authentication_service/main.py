#!/usr/bin/env python3
"""
 End-to-end integration test
"""

import requests


def register_user(email: str, password: str) -> None:
    """Registers a User"""
    payload = {"email": email, "password": password}
    resp = requests.post("http://127.0.0.1:5000/users", data=payload)
    assert resp.status_code == 200
    assert resp.json() == {"email": f"{email}", "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tries to log in with wrong password"""
    payload = {"email": email, "password": "439u43i32"}
    resp = requests.post("http://127.0.0.1:5000/sessions", data=payload)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tries to log in with right password"""
    payload = {"email": email, "password": password}
    resp = requests.post("http://127.0.0.1:5000/sessions", data=payload)
    assert resp.status_code == 200
    assert resp.json() == {"email": f"{email}", "message": "logged in"}
    return resp.cookies.get("session_id")


def profile_unlogged() -> None:
    """Unlog profile"""
    resp = requests.get("http://127.0.0.1:5000/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Profile of Logged session"""
    resp = requests.get(
        "http://127.0.0.1:5000/profile", cookies={"session_id": session_id}
    )
    assert resp.status_code == 200
    assert resp.json() == {"email": f"{EMAIL}"}


def log_out(session_id: str) -> None:
    """Log out the session"""
    resp = requests.delete(
        "http://127.0.0.1:5000/sessions", cookies={"session_id": session_id}
    )
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """Reset the password token"""
    payload = {"email": email}
    resp = requests.post("http://127.0.0.1:5000/reset_password", data=payload)
    assert resp.status_code == 200
    return resp.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates user password"""
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    resp = requests.put("http://127.0.0.1:5000/reset_password", data=payload)
    assert resp.status_code == 200
    assert resp.json() == {"email": f"{email}", "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
