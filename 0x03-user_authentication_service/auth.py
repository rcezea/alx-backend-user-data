#!/usr/bin/env python3
"""
Hash password module
"""
import bcrypt
from db import DB, NoResultFound, InvalidRequestError
from user import User
import uuid


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
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(
                email, hashed_password=_hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Login Validation"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """ create a session """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """Return user by session id"""
        try:
            if session_id:
                user = self._db.find_user_by(session_id=session_id)
                return user
            return None
        except NoResultFound:
            return None


def _generate_uuid() -> str:
    """Generate UUIDs"""
    return str(uuid.uuid4())
