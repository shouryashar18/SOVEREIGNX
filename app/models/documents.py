from pydantic import BaseModel
from typing import Optional


class DocumentResponse(BaseModel):
    id: str
    workspace_id: str
    filename: str
    file_type: str
    file_path: str
    status: str