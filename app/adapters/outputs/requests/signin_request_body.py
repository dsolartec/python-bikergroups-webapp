from pydantic import BaseModel, ConfigDict, Field


class SignInRequestBody(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    phone: str
    password: str
