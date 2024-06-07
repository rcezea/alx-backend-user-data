#!/usr/bin/env python3
""" Session manager
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session class for Session Manager"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create session id
        :param user_id:
        :return: session id
        """
        if isinstance(user_id, str):
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        lookup the user id from session_id
        :param session_id:
        :return: user id
        """
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """
        Lookup user by cookie value
        :param request:
        :return: user instance
        """
        if request:
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            return User.get(user_id)
        return None
