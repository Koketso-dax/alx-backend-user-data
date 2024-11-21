"""
E2E integration test module
"""
from requests import get, put, post, delete

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """User registration test"""
    # New user successfully created
    response = post(f"{BASE_URL}/users",
                    data={"email": email, "password": password})
    assert response.json() == {"email": email, "message": "user created"}
    assert response.status_code == 200

    # Email already associated with user
    response = post(f"{BASE_URL}/users",
                    data={"email": email, "password": password})
    assert response.json() == {"message": "email already registered"}
    assert response.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """Wrong password test"""
    response = post(f"{BASE_URL}/sessions",
                    data={"email": email, "password": password})
    assert response.status_code == 401
    assert response.cookies.get("session_id") is None


def log_in(email: str, password: str) -> str:
    """Login test
    Return:
        - session_id
    """
    response = post(f"{BASE_URL}/sessions",
                    data={"email": email, "password": password})
    session_id = response.cookies.get("session_id")
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Signed out user profile test"""
    response = get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Signed in user profile test"""
    response = get(f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Logout test"""
    response = delete(f"{BASE_URL}/sessions",
                      cookies={"session_id": session_id},
                      allow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.history[0].status_code == 302
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Reset token test
    Return:
        - reset token
    """
    response = post(f"{BASE_URL}/reset_password", data={"email": email})
    reset_token = response.json().get("reset_token")
    assert response.status_code == 200
    assert isinstance(reset_token, str)
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Password update test"""
    response = put(f"{BASE_URL}/reset_password",
                   data={"email": email, "new_password": new_password,
                         "reset_token": reset_token})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "password"
NEW_PASSWD = "P@ssword@47"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
