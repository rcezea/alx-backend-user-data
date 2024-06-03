#!/usr/bin/env python3
""" Basic Authentication manager
"""
import binascii

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """" Extract encoded string from header """
        if authorization_header:
            if isinstance(authorization_header, str):
                if authorization_header.startswith('Basic '):
                    return authorization_header.split()[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decode password from header """
        if base64_authorization_header:
            if isinstance(base64_authorization_header, str):
                try:
                    return base64.b64decode(
                        base64_authorization_header).decode('utf-8')
                except binascii.Error:
                    return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract user credentials from header """
        if decoded_base64_authorization_header:
            if isinstance(decoded_base64_authorization_header, str):
                try:
                    cred = decoded_base64_authorization_header.split(':')
                    if len(cred) == 2:
                        return cred[0], cred[1]
                    else:
                        return None, None
                except ValueError:
                    return None, None
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request """
        header = self.authorization_header(request)
        encoded_str = self.extract_base64_authorization_header(header)
        decoded_str = self.decode_base64_authorization_header(encoded_string)
        user, passw = self.extract_user_credentials(decoded_string)
        return self.user_object_from_credentials(user, passw)
