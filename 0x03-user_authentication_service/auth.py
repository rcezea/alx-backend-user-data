#!/usr/bin/env python3
"""
Hash password module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ hash the password """
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())
