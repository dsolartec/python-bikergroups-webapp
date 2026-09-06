from http import HTTPMethod

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.adapters.outputs.decorators.require_permissions import require_permissions
from app.adapters.outputs.decorators.require_unlogged import require_unlogged
from app.bootstrap import bootstrap
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException
from app.domain.models.roadtrip_model import RoadTripModel
from app.domain.models.user_model import UserModel


web_views = Blueprint("web_views", __name__)
message_bus = bootstrap()


@web_views.before_app_request
def load_logged_user_from_session():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
        return

    try:
        g.user = message_bus.handle(GetUserByIDCommand(id=user_id))
    except NotFoundException:
        session.clear()
        g.user = None


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


@web_views.route("/login", methods=[HTTPMethod.GET, HTTPMethod.POST])
@require_unlogged()
def signin_page():
    if request.method == HTTPMethod.POST:
        phone = request.form["phone"]
        password = request.form["password"]

        try:
            user: UserModel = message_bus.handle(SignInCommand(
                password=password,
                phone=phone
            ))

            session.clear()
            session["user_id"] = user.id

            return redirect(url_for("web_views.landing_page"))
        except WrongCredentialsException:
            flash("El número de teléfono o la contraseña no son válidos", "signin.error")

    return render_template("auth/signin.html")


@web_views.route("/logout", methods=[HTTPMethod.GET])
@require_permissions(permissions=[])
def signout_page():
    session.clear()
    return redirect(url_for("web_views.landing_page"))
