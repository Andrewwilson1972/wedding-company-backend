from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.services.auth_service import authenticate_admin, create_token_for_admin

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin: dict


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest):
    """
    Admin login endpoint.
    - Validates credentials
    - Returns a JWT access token with `sub` and `org` claims
    """
    admin = await authenticate_admin(payload.email, payload.password)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_token_for_admin(admin)
    admin_public = {"email": admin.get("email"), "organization_name": admin.get("organization_name")}
    return {"access_token": token, "token_type": "bearer", "admin": admin_public}
