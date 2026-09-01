from pydantic import BaseModel


class UserPermissionModel(BaseModel):
    id: str
    permission_id: str
    user_id: str
