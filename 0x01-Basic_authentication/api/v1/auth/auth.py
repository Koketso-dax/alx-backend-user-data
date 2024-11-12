#!/usr/bin/env python3
"""Used to handle authetication"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class to handle authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
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
