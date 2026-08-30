from pydantic import BaseModel, ConfigDict


class TokensResponse(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    access_token: str
    refresh_token: str
