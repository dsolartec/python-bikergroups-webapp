from flask import Blueprint, g, render_template, session

from app.adapters.outputs.decorators.require_permissions import require_permissions
from app.bootstrap import bootstrap
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.exceptions.not_found_exception import NotFoundException


admin_views = Blueprint("admin_views", __name__, url_prefix="/admin")
message_bus = bootstrap()


@admin_views.before_app_request
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
    return render_template("admin/index.html")
