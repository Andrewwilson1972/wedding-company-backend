from pydantic import BaseModel, Field
from typing import Optional


class OrganizationCreate(BaseModel):
    organization_name: str = Field(..., min_length=2, max_length=50)
    email: str
    password: str


class OrganizationInDB(BaseModel):
    id: Optional[str] = None
    organization_name: str
    collection_name: str
    admin_email: str

    model_config = {"from_attributes": True}
