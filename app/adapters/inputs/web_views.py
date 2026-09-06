from flask import Blueprint, render_template

from app.bootstrap import bootstrap
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.models.roadtrip_model import RoadTripModel


web_views = Blueprint("web_views", __name__)
message_bus = bootstrap()


@web_views.get("/")
def landing_page():
    recent_roadtrips: list[RoadTripModel]
    roadtrips_count: int

    recent_roadtrips, roadtrips_count, _ = message_bus.handle(GetAllRoadtripsPaginatedCommand(
        current_page=0,
        limit=5,
    ))

    return render_template(
        "index.html",
        recent_roadtrips={
            "first": recent_roadtrips[0],
            "rest": recent_roadtrips[1:],
        },
        roadtrips_count=roadtrips_count,
    )
