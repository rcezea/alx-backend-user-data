#!/usr/bin/env python3
""" Authentication manager
"""
from typing import List, TypeVar
from flask import request
from os import getenv


class Auth:
    """ Basic Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if auth is required"""
        if isinstance(path, str) and path:
            slash = str(path) + '/'
            if isinstance(excluded_paths, list) and excluded_paths:
                if slash in excluded_paths or path in excluded_paths:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current User """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Lookup and return cookie value
        :param request:
        :return: cookie value
        """
        if request is None:
            return None
        session_name = getenv("SESSION_NAME")
        return request.cookies.get(session_name)
