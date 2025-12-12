from app.core.security import hash_password, verify_password


def hash_user_password(password: str) -> str:
    """
    Wrapper for hashing user/admin passwords.
    Keeps utils separated from core logic.
    """
    return hash_password(password)


def check_password(password: str, hashed_password: str) -> bool:
    """
    Wrapper for verifying passwords.
    """
    return verify_password(password, hashed_password)
