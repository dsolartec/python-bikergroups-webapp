from pydantic import BaseModel


class PermissionModel(BaseModel):
    id: str
    name: str
