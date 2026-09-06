from http import HTTPMethod

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.adapters.outputs.decorators.require_permissions import require_permissions
from app.adapters.outputs.decorators.require_unlogged import require_unlogged
from app.bootstrap import bootstrap
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.phone_already_exists_exception import PhoneAlreadyExistsException
from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException


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
    recent_roadtrips, roadtrips_count, _ = message_bus.handle(GetAllRoadtripsPaginatedCommand(
        current_page=1,
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


@web_views.get("/roadtrips")
def roadtrips_page():
    current_page = request.args.get("page", default=1, type=int)

    page_roadtrips, total_roadtrips_count, max_pages = message_bus.handle(GetAllRoadtripsPaginatedCommand(
        current_page=current_page,
        limit=6,
    ))

    return render_template(
        "roadtrips.html",
        page_roadtrips=page_roadtrips,
        total_roadtrips_count=total_roadtrips_count,
        current_page=current_page,
        max_pages=max_pages,
    )


@web_views.route("/login", methods=[HTTPMethod.GET, HTTPMethod.POST])
@require_unlogged()
def signin_page():
    phone: str = ""
    password: str = ""

    if request.method == HTTPMethod.POST:
        phone = request.form["phone"]
        password = request.form["password"]

        try:
            user = message_bus.handle(SignInCommand(
                password=password,
                phone=phone
            ))

            session.clear()
            session["user_id"] = user.id

            return redirect(url_for("web_views.landing_page"))
        except WrongCredentialsException:
            flash("El número de teléfono o la contraseña no son válidos", "signin.error")

    return render_template(
        "auth.html",
        signin_form_data={
            "phone": phone,
            "password": password,
        },
        signup_form_data={},
    )


@web_views.route("/register", methods=[HTTPMethod.GET, HTTPMethod.POST])
@require_unlogged()
def signup_page():
    confirm_password: str = ""
    display_name: str = ""
    password: str = ""
    phone: str = ""

    if request.method == HTTPMethod.POST:
        flashed_message: bool = False

        display_name = request.form["display_name"]
        if len(display_name) < 4 or len(display_name) > 100:
            flash("El nombre visible debe tener entre 4 y 100 caracteres", "signup.display_name.error")
            flashed_message = True

        phone = request.form["phone"]
        if len(phone) != 10 or not phone.startswith("3"):
            flash("El número de teléfono no es válido", "signup.phone.error")
            flashed_message = True

        password = request.form["password"]
        if len(password) < 8:
            flash("La contraseña debe tener mínimo 8 caracteres", "signup.password.error")
            flashed_message = True
        elif len(password) > 80:
            flash("La contraseña solo puede tener máximo 80 caracteres", "signup.password.error")
            flashed_message = True
        else:
            numbers_count: int = 0
            lowers_count: int = 0
            uppers_count: int = 0

            for character in password:
                if character.isnumeric():
                    numbers_count += 1
                elif character.islower():
                    lowers_count += 1
                elif character.isupper():
                    uppers_count += 1

            if uppers_count == 0:
                flash("La contraseña debe tener mínimo una letra mayúscula", "signup.password.error")
                flashed_message = True
            elif lowers_count == 0:
                flash("La contraseña debe tener mínimo una letra minúscula", "signup.password.error")
                flashed_message = True
            elif numbers_count == 0:
                flash("La contraseña debe tener mínimo un número", "signup.password.error")
                flashed_message = True

        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            flash("Las contraseñas no coinciden", "signup.confirm_password.error")
            flashed_message = True

        if not flashed_message:
            try:
                user = message_bus.handle(SignUpCommand(
                    display_name=display_name,
                    password=password,
                    phone=phone
                ))

                session.clear()
                session["user_id"] = user.id

                return redirect(url_for("web_views.landing_page"))
            except PhoneAlreadyExistsException:
                flash("El número de teléfono ya está en uso", "signup.phone.error")

    return render_template(
        "auth.html",
        signin_form_data={},
        signup_form_data={
            "confirm_password": confirm_password,
            "display_name": display_name,
            "password": password,
            "phone": phone,
        },
    )


@web_views.route("/logout", methods=[HTTPMethod.GET])
@require_permissions(permissions=[])
def signout_page():
    session.clear()
    return redirect(url_for("web_views.landing_page"))
