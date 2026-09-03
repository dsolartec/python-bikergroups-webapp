from pydantic import BaseModel, ConfigDict, Field


class RefreshRequestBody(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    refresh_token: str
