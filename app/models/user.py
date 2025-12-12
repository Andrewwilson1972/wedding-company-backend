from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AdminCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class AdminInDB(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    organization_name: str
    is_admin: bool = True

    model_config = {"from_attributes": True}


class AdminPublic(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    organization_name: str

    model_config = {"from_attributes": True}
