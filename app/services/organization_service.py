from typing import Optional, Dict, Any

from app.core.database import get_db
from app.utils.password_handler import hash_user_password


# ---------------------------
# CREATE ORGANIZATION
# ---------------------------
async def create_organization(org_name: str, email: str, password: str) -> Dict[str, Any]:
    db = get_db()

    # Check if organization already exists in master db
    existing = await db["organizations"].find_one({"organization_name": org_name})
    if existing:
        return {"error": "Organization already exists"}

    # The dynamic collection for this organization
    collection_name = f"org_{org_name.lower()}"

    # Create admin user for this organization
    hashed_password = hash_user_password(password)

    admin_doc = {
        "email": email,
        "hashed_password": hashed_password,
        "organization_name": org_name,
        "is_admin": True,
    }

    # Insert admin into master admins collection
    admin_result = await db["admins"].insert_one(admin_doc)

    # Insert organization metadata into master organizations collection
    org_doc = {
        "organization_name": org_name,
        "collection_name": collection_name,
        "admin_email": email,
        "admin_id": str(admin_result.inserted_id),
    }

    await db["organizations"].insert_one(org_doc)

    # Create the dynamic collection for this organization
    # (MongoDB creates a collection automatically on first insert)
    await db[collection_name].insert_one({"initialized": True})

    return {
        "message": "Organization created successfully",
        "organization": org_doc,
        "admin": {"email": email},
    }


# ---------------------------
# GET ORGANIZATION BY NAME
# ---------------------------
async def get_organization_by_name(org_name: str) -> Optional[Dict[str, Any]]:
    db = get_db()
    org = await db["organizations"].find_one({"organization_name": org_name})
    return org


# ---------------------------
# UPDATE ORGANIZATION
# ---------------------------
async def update_organization(org_name: str, new_email: str, new_password: str) -> Dict[str, Any]:
    db = get_db()

    # Check if organization exists
    org = await db["organizations"].find_one({"organization_name": org_name})
    if not org:
        return {"error": "Organization not found"}

    # Update admin user
    hashed_pw = hash_user_password(new_password)
    await db["admins"].update_one(
        {"email": org["admin_email"]},
        {"$set": {"email": new_email, "hashed_password": hashed_pw}},
    )

    # Update organization metadata
    await db["organizations"].update_one(
        {"organization_name": org_name},
        {"$set": {"admin_email": new_email}},
    )

    return {"message": "Organization updated successfully"}


# ---------------------------
# DELETE ORGANIZATION
# ---------------------------
async def delete_organization(org_name: str, requesting_admin_email: str) -> Dict[str, Any]:
    db = get_db()

    # Verify org exists
    org = await db["organizations"].find_one({"organization_name": org_name})
    if not org:
        return {"error": "Organization not found"}

    # ONLY allow deletion by admin of that org
    if org["admin_email"] != requesting_admin_email:
        return {"error": "Unauthorized deletion attempt"}

    collection_name = org["collection_name"]

    # Delete organization metadata
    await db["organizations"].delete_one({"organization_name": org_name})

    # Delete admin user
    await db["admins"].delete_one({"email": org["admin_email"]})

    # Drop dynamic collection
    await db.drop_collection(collection_name)

    return {"message": "Organization deleted successfully"}
