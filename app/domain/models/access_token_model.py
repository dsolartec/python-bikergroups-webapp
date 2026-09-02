from pydantic import BaseModel, ConfigDict, Field


class AccessTokenModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        serialize_by_alias=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

    expiration_timestamp: int = Field(alias="exp")
    generation_timestamp: int = Field(alias="iat")
    permissions_names: list[str] = Field(alias="permissions")
    user_id: str = Field(alias="sub")
    username: str
