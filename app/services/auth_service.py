from typing import Optional, Dict, Any

from app.utils.password_handler import check_password
from app.utils.jwt_handler import create_jwt_token
from app.core.database import get_db


async def get_admin_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Fetch admin document from the master 'admins' collection by email.
    Returns None if not found.
    """
    db = get_db()
    admins_coll = db.get_collection("admins")
    admin = await admins_coll.find_one({"email": email})
    return admin


async def authenticate_admin(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Verify admin credentials. Returns the admin document on success, otherwise None.
    """
    admin = await get_admin_by_email(email)
    if not admin:
        return None

    hashed = admin.get("hashed_password") or admin.get("password_hash")  # support possible field names
    if not hashed:
        return None

    if not check_password(password, hashed):
        return None

    return admin


def create_token_for_admin(admin: Dict[str, Any], expires_minutes: Optional[int] = None) -> str:
    """
    Create a JWT token for a validated admin.
    Token will include:
      - sub: admin id (or email if id not present)
      - org: organization_name
    """
    subject = str(admin.get("_id")) if admin.get("_id") is not None else admin.get("email")
    org = admin.get("organization_name") or admin.get("org") or ""
    token = create_jwt_token(subject=subject, org=org, expires_minutes=expires_minutes)
    return token
