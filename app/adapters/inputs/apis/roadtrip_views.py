from http import HTTPStatus

from flask import Blueprint, request

from app.adapters.outputs.decorators.authenticator import authenticator
from app.adapters.outputs.requests.create_one_roadtrip_request_body import CreateOneRoadTripRequestBody
from app.bootstrap import bootstrap
from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand
from app.domain.models.access_token_model import AccessTokenModel
from app.domain.models.roadtrip_model import RoadTripModel


roadtrip_views = Blueprint("roadtrip_views", __name__, url_prefix="/api/roadtrip")
message_bus = bootstrap()


@roadtrip_views.post("/")
@authenticator(permission_names=["create_roadtrip"])
def create_roadtrip(logged_access_token: AccessTokenModel):
    payload = CreateOneRoadTripRequestBody.model_validate(request.get_json(silent=True) or {})

    roadtrip: RoadTripModel = message_bus.handle(CreateOneRoadTripCommand(
        display_name=payload.display_name,

        start_at=payload.start_at,
        start_coordinates=payload.start_coordinates,

        end_coordinates=payload.end_coordinates,

        actor_id=logged_access_token.user_id,
    ))

    return roadtrip.model_dump(include=["id"]), HTTPStatus.CREATED


@roadtrip_views.put("/<string:roadtrip_id>/photo")
@authenticator(permission_names=["update_roadtrip"])
def update_roadtrip_photo(
        roadtrip_id: str,
        logged_access_token: AccessTokenModel,
):
    message_bus.handle(UpdateRoadTripPhotoCommand(
        actor_id=logged_access_token.user_id,
        roadtrip_id=roadtrip_id,
    ))

    return "", HTTPStatus.NO_CONTENT
