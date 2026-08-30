from pydantic import BaseModel, ConfigDict, Field


class SignUpRequestBody(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    username: str = Field(min_length=4, max_length=20, pattern=r"^[a-zA-Z0-9_-]+$")
    password: str = Field(min_length=8, max_length=80)
    confirm_password: str = Field(min_length=8, max_length=80)

    display_name: str = Field(min_length=4, max_length=100)
