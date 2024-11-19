#!/usr/bin/env python3
"""Auth module"""


import logging
from typing import Union
from uuid import uuid4
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User

logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt
    Args:
        password (str): The password to hash
    Returns:
        bytes: The hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a unique UUID
    Returns:
        str: A unique UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with database"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user in the database
        Args:
            email (str): The email of the user
            password (str): The password of the user
        Returns:
            User: The newly created user
        Raises:
            ValueError: If a user with the same email already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user credentials
        Args:
            email (str): The email of the user
            password (str): The password of the user
        Returns:
            bool: True if the credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session for the user
        Args:
            email (str): The email of the user
        Returns:
            str: The session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Gets the user from the session ID
        Args:
            session_id (str): The session ID
        Returns:
            User: The user if found, None otherwise
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session for the user
        Args:
            user_id (int): The ID of the user
        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for the user
        Args:
            email (str): The email of the user
        Returns:
            str: The reset password token
        Raises:
            ValueError: If the user is not found
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"User {email} not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password
        Args:
            reset_token (str): The reset password token
            password (str): The new password
        Raises:
            ValueError: If the reset token is invalid
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")
