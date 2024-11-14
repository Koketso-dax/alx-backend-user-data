#!/usr/bin/env python3
"""Session Authentication Expiration"""
from session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Expiration Authentication class"""
    def __init__(self):
        """Initialize Session Expiration Authentication"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for session ID"""
        if session_id is None:
            return None
        user_session = self.user_id_by_session_id.get(session_id)
        if user_session is None:
            return None
        if self.session_duration <= 0:
            return user_session.get('user_id')
        created_at = user_session.get('created_at')
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return user_session.get('user_id')
