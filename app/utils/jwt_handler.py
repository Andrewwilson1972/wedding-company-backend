from typing import Dict, Any, Optional

from jose import JWTError

from app.core.security import create_access_token, decode_access_token
from app.core.config import settings


def create_jwt_token(subject: str, org: str, expires_minutes: Optional[int] = None) -> str:
    """
    Create a JWT token with minimal claims.
    `subject` should be a unique identifier for the admin (e.g., admin id or email).
    `org` is the organization identifier/name.
    """
    payload: Dict[str, Any] = {"sub": subject, "org": org}
    token = create_access_token(payload, expires_minutes)
    return token


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate the JWT token.
    Raises JWTError if invalid/expired.
    """
    try:
        data = decode_access_token(token)
        return data
    except JWTError as e:
        # Re-raise so routers/services can catch and return proper HTTP errors
        raise e


def get_token_from_header(authorization_header: Optional[str]) -> Optional[str]:
    """
    Extract token from an Authorization header of the form: "Bearer <token>"
    Returns None if header is missing or malformed.
    """
    if not authorization_header:
        return None
    parts = authorization_header.split()
    if len(parts) != 2:
        return None
    scheme, token = parts
    if scheme.lower() != "bearer":
        return None
    return token
