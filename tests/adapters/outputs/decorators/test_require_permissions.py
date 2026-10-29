from datetime import datetime
import unittest

from flask import Flask, g

from app.adapters.outputs.decorators.require_permissions import require_permissions
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.permission_model import PermissionModel
from app.domain.models.user_model import UserModel


class TestRequirePermissions(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_redirects_when_user_is_none(self):
        @require_permissions(permissions=[PermissionEnum.CAN_CREATE_ROADTRIP], redirect_to="/login")
        def protected_view():
            return "allowed"

        with self.app.test_request_context("/admin"):
            g.user = None
            res = protected_view()
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "/login")

    def test_allows_when_permissions_list_is_empty_and_user_logged_in(self):
        @require_permissions(permissions=[])
        def protected_view():
            return "allowed"

        with self.app.test_request_context("/logout"):
            g.user = UserModel(
                id="018f1234-5678-7000-8000-000000000001",
                phone="3001234567",
                display_name="User",
                created_at=datetime(2026, 1, 1, 10, 0, 0),
                updated_at=datetime(2026, 1, 1, 10, 0, 0),
                permissions=[],
            )
            res = protected_view()
            self.assertEqual(res, "allowed")

    def test_allows_when_user_has_required_permission(self):
        @require_permissions(permissions=[PermissionEnum.CAN_CREATE_ROADTRIP])
        def protected_view():
            return "allowed"

        with self.app.test_request_context("/admin"):
            g.user = UserModel(
                id="018f1234-5678-7000-8000-000000000001",
                phone="3001234567",
                display_name="Admin",
                created_at=datetime(2026, 1, 1, 10, 0, 0),
                updated_at=datetime(2026, 1, 1, 10, 0, 0),
                permissions=[
                    PermissionModel(
                        id="018f1234-5678-7000-8000-000000000010",
                        name=PermissionEnum.CAN_CREATE_ROADTRIP,
                    )
                ],
            )
            res = protected_view()
            self.assertEqual(res, "allowed")

    def test_redirects_when_user_lacks_required_permission(self):
        @require_permissions(permissions=[PermissionEnum.CAN_UPDATE_ROADTRIP], redirect_to="/")
        def protected_view():
            return "allowed"

        with self.app.test_request_context("/admin"):
            g.user = UserModel(
                id="018f1234-5678-7000-8000-000000000001",
                phone="3001234567",
                display_name="User",
                created_at=datetime(2026, 1, 1, 10, 0, 0),
                updated_at=datetime(2026, 1, 1, 10, 0, 0),
                permissions=[
                    PermissionModel(
                        id="018f1234-5678-7000-8000-000000000010",
                        name=PermissionEnum.CAN_CREATE_ROADTRIP,
                    )
                ],
            )
            res = protected_view()
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "/")

