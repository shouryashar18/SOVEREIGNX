from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceLogin
)
from uuid import uuid4


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


# =========================================================
# CREATE WORKSPACE
# =========================================================

@router.post("/")
def create_workspace(workspace: WorkspaceCreate):

    # Check existing email
    existing_email = db.workspaces.find_one({
        "email": workspace.email
    })

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Check existing organization ID
    existing_org = db.workspaces.find_one({
        "organization_id": workspace.organization_id
    })

    if existing_org:
        raise HTTPException(
            status_code=400,
            detail="Organization ID already exists"
        )

    workspace_id = str(uuid4())

    workspace_data = {
        "id": workspace_id,
        "name": workspace.name,
        "email": workspace.email,
        "organization_id": workspace.organization_id,
        "password": workspace.password,
        "admin_name": workspace.admin_name,
        "industry": workspace.industry
    }

    db.workspaces.insert_one(workspace_data)

    return {
        "message": "Workspace created successfully",
        "workspace": {
            "id": workspace_id,
            "name": workspace.name,
            "email": workspace.email,
            "organization_id": workspace.organization_id,
            "admin_name": workspace.admin_name,
            "industry": workspace.industry
        }
    }


# =========================================================
# GET ALL WORKSPACES
# =========================================================

@router.get("/")
def get_workspaces():

    workspaces = []

    for workspace in db.workspaces.find({}, {"_id": 0}):

        workspaces.append({
            "id": workspace.get("id"),
            "name": workspace.get("name"),
            "email": workspace.get("email"),
            "organization_id": workspace.get("organization_id"),
            "admin_name": workspace.get("admin_name"),
            "industry": workspace.get("industry")
        })

    return {
        "workspaces": workspaces
    }


# =========================================================
# GET SINGLE WORKSPACE
# =========================================================

@router.get("/{workspace_id}")
def get_workspace(workspace_id: str):

    workspace = db.workspaces.find_one(
        {"id": workspace_id},
        {"_id": 0}
    )

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return {
        "id": workspace.get("id"),
        "name": workspace.get("name"),
        "email": workspace.get("email"),
        "organization_id": workspace.get("organization_id"),
        "admin_name": workspace.get("admin_name"),
        "industry": workspace.get("industry")
    }


# =========================================================
# UPDATE WORKSPACE
# =========================================================

@router.put("/{workspace_id}")
def update_workspace(
    workspace_id: str,
    workspace: WorkspaceUpdate
):

    update_data = {}

    if workspace.name is not None:
        update_data["name"] = workspace.name

    if workspace.industry is not None:
        update_data["industry"] = workspace.industry

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    result = db.workspaces.update_one(
        {"id": workspace_id},
        {
            "$set": update_data
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    updated_workspace = db.workspaces.find_one(
        {"id": workspace_id},
        {"_id": 0}
    )

    return {
        "message": "Workspace updated successfully",
        "workspace": {
            "id": updated_workspace.get("id"),
            "name": updated_workspace.get("name"),
            "email": updated_workspace.get("email"),
            "organization_id": updated_workspace.get("organization_id"),
            "admin_name": updated_workspace.get("admin_name"),
            "industry": updated_workspace.get("industry")
        }
    }


# =========================================================
# DELETE WORKSPACE
# =========================================================

@router.delete("/{workspace_id}")
def delete_workspace(workspace_id: str):

    result = db.workspaces.delete_one({
        "id": workspace_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return {
        "message": "Workspace deleted successfully",
        "workspace_id": workspace_id
    }


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login_workspace(data: WorkspaceLogin):

    workspace = db.workspaces.find_one({
        "email": data.email,
        "password": data.password
    })

    if not workspace:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "workspace_id": workspace.get("id"),
        "organization_id": workspace.get("organization_id"),
        "name": workspace.get("name"),
        "email": workspace.get("email"),
        "admin_name": workspace.get("admin_name"),
        "industry": workspace.get("industry")
    }