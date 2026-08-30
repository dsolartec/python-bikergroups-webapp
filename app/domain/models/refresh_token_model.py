from pydantic import BaseModel, ConfigDict, Field


class RefreshTokenModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        serialize_by_alias=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

    expiration_timestamp: int = Field(alias="exp")
    generation_timestamp: int = Field(alias="iat")
    user_id: str = Field(alias="sub")
