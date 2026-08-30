from http import HTTPStatus

from flask import Blueprint, request

from app.adapters.outputs.requests.signup_request_body import SignUpRequestBody
from app.adapters.outputs.responses.tokens_response import TokensResponse
from app.bootstrap import bootstrap
from app.domain.commands.signup_command import SignUpCommand


auth_views = Blueprint("auth_views", __name__, url_prefix="/api/auth")
message_bus = bootstrap()


@auth_views.post("/signup")
def signup():
    payload = SignUpRequestBody.model_validate(request.get_json(silent=True) or {})

    access_token: str
    refresh_token: str

    access_token, refresh_token = message_bus.handle(SignUpCommand(
        display_name=payload.display_name,
        password=payload.password,
        username=payload.username,
    ))

    return TokensResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    ).model_dump(), HTTPStatus.CREATED
