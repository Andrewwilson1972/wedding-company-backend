from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel

from app.services.organization_service import (
    create_organization,
    get_organization_by_name,
    update_organization,
    delete_organization
)
from app.utils.jwt_handler import decode_jwt_token, get_token_from_header


router = APIRouter()


# ---------------------------
# Request Models
# ---------------------------
class OrgCreateRequest(BaseModel):
    organization_name: str
    email: str
    password: str


class OrgUpdateRequest(BaseModel):
    organization_name: str
    email: str
    password: str


class OrgDeleteRequest(BaseModel):
    organization_name: str


# ---------------------------
# CREATE ORG
# ---------------------------
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_org(payload: OrgCreateRequest):
    result = await create_organization(
        org_name=payload.organization_name,
        email=payload.email,
        password=payload.password
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


# ---------------------------
# GET ORG BY NAME
# ---------------------------
@router.get("/get")
async def get_org(organization_name: str):
    org = await get_organization_by_name(organization_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


# ---------------------------
# UPDATE ORG
# ---------------------------
@router.put("/update")
async def update_org(payload: OrgUpdateRequest, authorization: str = Header(None)):
    token = get_token_from_header(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    decoded = decode_jwt_token(token)
    admin_org = decoded.get("org")

    if admin_org != payload.organization_name:
        raise HTTPException(status_code=403, detail="You are not authorized to update this organization.")

    result = await update_organization(
        org_name=payload.organization_name,
        new_email=payload.email,
        new_password=payload.password
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


# ---------------------------
# DELETE ORG
# ---------------------------
@router.delete("/delete")
async def delete_org(payload: OrgDeleteRequest, authorization: str = Header(None)):
    token = get_token_from_header(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    decoded = decode_jwt_token(token)
    admin_email = decoded.get("sub")
    org_name = payload.organization_name

    result = await delete_organization(
        org_name=org_name,
        requesting_admin_email=admin_email
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
