#!/usr/bin/env python3
"""Session db module"""
from session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session db auth class"""
    def create_session(self, user_id=None):
        """Create session"""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id from session id"""
        try:
            sessions = UserSession.search(session_id=session_id)
            if sessions:
                current_time = datetime.now()
                time_elapsed = timedelta(
                    seconds=self.session_duration
                )  # session_duration is inherited from SessionExpAuth
                if sessions[0].created_at + time_elapsed < current_time:
                    return None
                return sessions[0].user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """Destroy session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user_session = UserSession.search(session_id=session_id)
        if user_session:
            user_session[0].remove()
        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
