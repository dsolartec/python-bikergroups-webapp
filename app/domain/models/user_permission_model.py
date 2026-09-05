from pydantic import BaseModel, Field


class UserPermissionModel(BaseModel):
    id: str | None = Field(default=None)
    permission_id: str
    user_id: str
