from pydantic import BaseModel, EmailStr


class WorkspaceCreate(BaseModel):
    name: str
    email: EmailStr
    organization_id: str
    password: str
    admin_name: str
    industry: str


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    email: str
    organization_id: str
    admin_name: str
    industry: str


class WorkspaceUpdate(BaseModel):
    name: str
    industry: str

class WorkspaceLogin(BaseModel):
    email: EmailStr
    password: str