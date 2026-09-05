from http import HTTPStatus

from flask import Blueprint, request

from app.adapters.outputs.decorators.authenticator import authenticator
from app.adapters.outputs.requests.refresh_request_body import RefreshRequestBody
from app.adapters.outputs.requests.signin_request_body import SignInRequestBody
from app.adapters.outputs.requests.signup_request_body import SignUpRequestBody
from app.adapters.outputs.responses.tokens_response import TokensResponse
from app.bootstrap import bootstrap
from app.domain.commands.refresh_command import RefreshTokenCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.models.access_token_model import AccessTokenModel


auth_views = Blueprint("auth_views", __name__, url_prefix="/api/auth")
message_bus = bootstrap()


@auth_views.post("/refresh")
@authenticator(permissions=[], do_time_check=False)
def refresh_token(logged_access_token: AccessTokenModel):
    payload = RefreshRequestBody.model_validate(request.get_json(silent=True) or {})

    access_token: str
    refresh_token: str

    access_token, refresh_token = message_bus.handle(RefreshTokenCommand(
        refresh_token=payload.refresh_token,
    ))

    return TokensResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    ).model_dump(), HTTPStatus.OK


@auth_views.post("/signin")
def signin():
    payload = SignInRequestBody.model_validate(request.get_json(silent=True) or {})

    access_token: str
    refresh_token: str

    access_token, refresh_token = message_bus.handle(SignInCommand(
        password=payload.password,
        phone=payload.phone,
    ))

    return TokensResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    ).model_dump(), HTTPStatus.OK


@auth_views.post("/signup")
def signup():
    payload = SignUpRequestBody.model_validate(request.get_json(silent=True) or {})

    access_token: str
    refresh_token: str

    access_token, refresh_token = message_bus.handle(SignUpCommand(
        display_name=payload.display_name,
        password=payload.password,
        phone=payload.phone,
    ))

    return TokensResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    ).model_dump(), HTTPStatus.CREATED
