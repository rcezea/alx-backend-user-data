#!/usr/bin/env python3
""" Creation of the BasicAuth class """

from .auth import Auth
from models.base import DATA
from models.user import User
from flask import request
from typing import Tuple, TypeVar
import base64


class BasicAuth(Auth):
    """A BasicAuth class"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extract from Authorization header the username and password
        Returns:
            Base64 encoded string of authorization header
        """
        if (
            authorization_header
            and isinstance(authorization_header, str)
            and authorization_header.startswith("Basic ")
        ):
            return authorization_header.split()[1]

        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decodes the value of the authorization header
        Return:
            decoded value of a Base64 string base64_authorization_header
        """
        if base64_authorization_header and isinstance(
            base64_authorization_header, str
        ):
            try:
                return base64.b64decode(
                    base64_authorization_header, validate=True
                ).decode("utf8")
            except Exception:
                return None
        return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str]:
        """A method that must get the user credentials
        Return:
            user email and password from the Base64 decoded value
        """
        if (
            decoded_base64_authorization_header
            and isinstance(decoded_base64_authorization_header, str)
            and ":" in decoded_base64_authorization_header
        ):
            (
                email,
                sep,
                password,
            ) = decoded_base64_authorization_header.partition(":")
            return (email, password)

        return (None, None)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """Get the user object from credentials
        Return:
            The user object from credentials
        """
        if user_email and user_pwd and DATA:
            user_obj = User.search({"email": user_email})
            if user_obj and user_obj[0].is_valid_password(user_pwd):
                return user_obj[0]
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Overload auth and retrive a User istance from a request
        Return:
            Retrives a user instance if possible
        """
        auth_key = self.authorization_header(request)
        if auth_key:
            encoded_credentials = self.extract_base64_authorization_header(
                auth_key
            )
            decoded_credentials = self.decode_base64_authorization_header(
                encoded_credentials
            )
            user_email, user_pass = self.extract_user_credentials(
                decoded_credentials
            )
            user_obj = self.user_object_from_credentials(user_email, user_pass)
            return user_obj