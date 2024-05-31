#!/usr/bin/env python3
"""A module that encypts passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """The function hashes the password"""
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the password is valid"""
    return bcrypt.checkpw(password.encode("utf8"), hashed_password)
