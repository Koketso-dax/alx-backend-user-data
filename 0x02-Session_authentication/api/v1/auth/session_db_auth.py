#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """
        Create and store a new instance of UserSession
        and return the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        storage.new(user_session)
        storage.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the User ID by requesting UserSession in the
        database based on session_id
        """
        if session_id is None:
            return None

        user_sessions = storage.all(UserSession).values()
        for user_session in user_sessions:
            if user_session.session_id == session_id:
                return user_session.user_id

        return None

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the Session ID from the request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = storage.all(UserSession).values()
        for user_session in user_sessions:
            if user_session.session_id == session_id:
                storage.delete(user_session)
                storage.save()
                return True

        return False
