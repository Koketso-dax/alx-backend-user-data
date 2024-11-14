#!/usr/bin/env python3
"""Used to handle authetication"""
from os import getenv
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class to handle authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths to
            exclude from authentication.
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # Remove the wildcard character
                base_excluded_path = excluded_path[:-1]
                if path.startswith(base_excluded_path):
                    return False
            else:
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> type:
        """Handle current User
           Returns:
                TypeVar: User
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request

        Args:
            request (request_object, optional): request. Defaults to None.
        """
        if request is None:
            return None

        session_name = getenv('SESSION_NAME')

        if session_name is None:
            return None

        return request.cookies.get(session_name)
