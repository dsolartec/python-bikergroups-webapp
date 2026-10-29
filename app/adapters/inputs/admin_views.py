from http import HTTPMethod

from flask import Blueprint, g, render_template, request, session

from app.adapters.outputs.decorators.require_permissions import require_permissions
from app.bootstrap import bootstrap
from app.domain.commands.delete_one_roadtrip_command import DeleteOneRoadTripCommand
from app.domain.commands.get_admin_stats_command import GetAdminStatsCommand
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_all_users_paginated_command import GetAllUsersPaginatedCommand
from app.domain.commands.get_roadtrip_by_id_command import GetRoadTripByIDCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.exceptions.not_found_exception import NotFoundException


admin_views = Blueprint("admin_views", __name__, url_prefix="/admin")
message_bus = bootstrap()


@admin_views.before_request
def load_logged_user_from_session():
    g.in_hk = True

    user_id = session.get("user_id")
    if user_id is None:
        g.can_hk = False
        g.user = None
        return

    try:
        g.can_hk = False
        g.user = message_bus.handle(GetUserByIDCommand(id=user_id, with_permissions=True))

        user_permissions = [up.name for up in g.user.permissions]
        for permission in [PermissionEnum.CAN_CREATE_ROADTRIP, PermissionEnum.CAN_UPDATE_ROADTRIP]:
            if permission in user_permissions:
                g.can_hk = True
                break
    except NotFoundException:
        session.clear()

        g.can_hk = False
        g.user = None


@admin_views.get("/")
@require_permissions(permissions=[PermissionEnum.CAN_CREATE_ROADTRIP, PermissionEnum.CAN_UPDATE_ROADTRIP])
def index_admin_page():
    total_upcoming_roadtrips, total_users = message_bus.handle(GetAdminStatsCommand())

    return render_template(
        "admin/index.html",
        upcoming_roadtrips_count=total_upcoming_roadtrips,
        registered_users_count=total_users,
    )


@admin_views.route("/roadtrips", methods=[HTTPMethod.GET, HTTPMethod.POST])
@require_permissions(permissions=[PermissionEnum.CAN_CREATE_ROADTRIP, PermissionEnum.CAN_UPDATE_ROADTRIP])
def roadtrips_admin_page():
    if request.method == HTTPMethod.POST.value:
        roadtrip_id = request.form.get("roadtrip_id", type=str)

        message_bus.handle(DeleteOneRoadTripCommand(
            actor_id=g.user.id,
            roadtrip_id=roadtrip_id,
        ))

    current_page = request.args.get("page", default=1, type=int)

    page_roadtrips, _, max_pages = message_bus.handle(GetAllRoadtripsPaginatedCommand(
        current_page=current_page,
        limit=10,
    ))

    return render_template(
        "admin/roadtrips.html",
        roadtrips=page_roadtrips,
        current_page=current_page,
        max_pages=max_pages,
    )


@admin_views.route("/roadtrips/create", methods=[HTTPMethod.GET, HTTPMethod.POST])
@require_permissions(permissions=[PermissionEnum.CAN_CREATE_ROADTRIP])
def create_roadtrip_admin_page():
    return render_template(
        "admin/roadtrip_form.html",
        mode="create",
        roadtrip=None,
    )


@admin_views.route("/roadtrips/<string:roadtrip_id>/edit", methods=[HTTPMethod.GET, HTTPMethod.POST])
@require_permissions(permissions=[PermissionEnum.CAN_UPDATE_ROADTRIP])
def edit_roadtrip_admin_page(roadtrip_id: str):
    roadtrip = message_bus.handle(GetRoadTripByIDCommand(
        id=roadtrip_id,
    ))

    return render_template(
        "admin/roadtrip_form.html",
        mode="edit",
        roadtrip=roadtrip,
    )


@admin_views.get("/users")
@require_permissions(permissions=[PermissionEnum.CAN_CREATE_ROADTRIP, PermissionEnum.CAN_UPDATE_ROADTRIP])
def users_admin_page():
    current_page = request.args.get("page", default=1, type=int)

    page_users, _, max_pages = message_bus.handle(GetAllUsersPaginatedCommand(
        current_page=current_page,
        limit=10,
    ))

    return render_template(
        "admin/users.html",
        users=page_users,
        current_page=current_page,
        max_pages=max_pages,
    )
