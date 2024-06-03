#!/usr/bin/env python3
""" Authentication manager
"""
from typing import List, TypeVar
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:

        if isinstance(path, str) and path:
            slash = str(path) + '/'
            if isinstance(excluded_paths, list) and excluded_paths:
                if slash in excluded_paths or path in excluded_paths:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
