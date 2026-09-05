from http import HTTPStatus

from flask import Blueprint

from app.adapters.outputs.responses.paginated_response import PaginatedResponse
from app.bootstrap import bootstrap
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.models.roadtrip_model import RoadTripModel


roadtrips_views = Blueprint("roadtrips_views", __name__, url_prefix="/api/roadtrips")
message_bus = bootstrap()


@roadtrips_views.get("/recent")
def get_recent_roadtrips():
    roadtrips: list[RoadTripModel]
    total_count: int

    roadtrips, total_count, _ = message_bus.handle(GetAllRoadtripsPaginatedCommand(
        current_page=0,
        limit=5,
    ))

    return PaginatedResponse[RoadTripModel](
        data=roadtrips,
        max_pages=1,
        total_count=min(5, total_count),
    ).model_dump(exclude={
        "data": {
            "__all__": {
                "created_at",
                "created_by",
                "updated_at",
                "updated_by",
            },
        },
    }), HTTPStatus.OK
