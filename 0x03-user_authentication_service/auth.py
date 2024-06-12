#!/usr/bin/env python3
"""
Hash password module
"""
import bcrypt
from db import DB, NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """ hash the password """
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user to the database """
        db = self._db
        try:
            user = db.find_user_by(email=email, hashed_password=password)
            raise ValueError("User {} already exists".format(user.email))
        except NoResultFound:
            password = _hash_password(password)
            user = db.add_user(email, password)
            return user