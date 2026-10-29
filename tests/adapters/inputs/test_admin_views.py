from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask, g, session

from app.adapters.inputs.admin_views import (
    admin_views,
    create_roadtrip_admin_page,
    edit_roadtrip_admin_page,
    index_admin_page,
    load_logged_user_from_session,
    roadtrips_admin_page,
    users_admin_page,
)
from app.domain.commands.delete_one_roadtrip_command import DeleteOneRoadTripCommand
from app.domain.commands.get_admin_stats_command import GetAdminStatsCommand
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_all_users_paginated_command import GetAllUsersPaginatedCommand
from app.domain.commands.get_roadtrip_by_id_command import GetRoadTripByIDCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.models.permission_model import PermissionModel
from app.domain.models.user_model import UserModel


class TestAdminViews(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "test-secret"
        self.app.register_blueprint(admin_views)

        self.admin_user = UserModel(
            id="018f1234-5678-7000-8000-000000000001",
            phone="3001234567",
            display_name="Admin User",
            created_at=datetime(2026, 1, 1, 10, 0, 0),
            updated_at=datetime(2026, 1, 1, 10, 0, 0),
            permissions=[
                PermissionModel(
                    id="018f1234-5678-7000-8000-000000000010",
                    name=PermissionEnum.CAN_CREATE_ROADTRIP,
                ),
                PermissionModel(
                    id="018f1234-5678-7000-8000-000000000011",
                    name=PermissionEnum.CAN_UPDATE_ROADTRIP,
                ),
            ],
        )

    def test_load_logged_user_from_session_unlogged(self):
        with self.app.test_request_context("/admin/"):
            load_logged_user_from_session()
            self.assertTrue(g.in_hk)
            self.assertFalse(g.can_hk)
            self.assertIsNone(g.user)

    @patch("app.adapters.inputs.admin_views.message_bus")
    def test_load_logged_user_from_session_with_admin_permissions(self, mock_bus):
        mock_bus.handle.return_value = self.admin_user

        with self.app.test_request_context("/admin/"):
            session["user_id"] = self.admin_user.id
            load_logged_user_from_session()

            self.assertTrue(g.in_hk)
            self.assertTrue(g.can_hk)
            self.assertEqual(g.user, self.admin_user)
            mock_bus.handle.assert_called_once_with(
                GetUserByIDCommand(id=self.admin_user.id, with_permissions=True)
            )

    @patch("app.adapters.inputs.admin_views.message_bus")
    def test_load_logged_user_from_session_not_found_clears_session(self, mock_bus):
        mock_bus.handle.side_effect = NotFoundException("User not found")

        with self.app.test_request_context("/admin/"):
            session["user_id"] = "missing-id"
            load_logged_user_from_session()

            self.assertFalse(g.can_hk)
            self.assertIsNone(g.user)
            self.assertNotIn("user_id", session)

    @patch("app.adapters.inputs.admin_views.render_template")
    @patch("app.adapters.inputs.admin_views.message_bus")
    def test_index_admin_page(self, mock_bus, mock_render):
        mock_bus.handle.return_value = (5, 12)
        mock_render.return_value = "rendered_admin_index"

        with self.app.test_request_context("/admin/"):
            g.user = self.admin_user
            res = index_admin_page()

            self.assertEqual(res, "rendered_admin_index")
            mock_bus.handle.assert_called_once_with(GetAdminStatsCommand())
            mock_render.assert_called_once_with(
                "admin/index.html",
                upcoming_roadtrips_count=5,
                registered_users_count=12,
            )

    @patch("app.adapters.inputs.admin_views.render_template")
    @patch("app.adapters.inputs.admin_views.message_bus")
    def test_roadtrips_admin_page_get_and_post(self, mock_bus, mock_render):
        mock_bus.handle.side_effect = [None, ([], 0, 0)]
        mock_render.return_value = "rendered_roadtrips"

        with self.app.test_request_context(
            "/admin/roadtrips?page=2",
            method="POST",
            data={"roadtrip_id": "rt-1"},
        ):
            g.user = self.admin_user
            res = roadtrips_admin_page()

            self.assertEqual(res, "rendered_roadtrips")
            mock_bus.handle.assert_any_call(
                DeleteOneRoadTripCommand(actor_id=self.admin_user.id, roadtrip_id="rt-1")
            )
            mock_bus.handle.assert_any_call(
                GetAllRoadtripsPaginatedCommand(current_page=2, limit=10)
            )
            mock_render.assert_called_once_with(
                "admin/roadtrips.html",
                roadtrips=[],
                current_page=2,
                max_pages=0,
            )

    @patch("app.adapters.inputs.admin_views.render_template")
    def test_create_roadtrip_admin_page(self, mock_render):
        mock_render.return_value = "rendered_create_form"

        with self.app.test_request_context("/admin/roadtrips/create"):
            g.user = self.admin_user
            res = create_roadtrip_admin_page()

            self.assertEqual(res, "rendered_create_form")
            mock_render.assert_called_once_with(
                "admin/roadtrip_form.html",
                mode="create",
                roadtrip=None,
            )

    @patch("app.adapters.inputs.admin_views.render_template")
    @patch("app.adapters.inputs.admin_views.message_bus")
    def test_edit_roadtrip_admin_page(self, mock_bus, mock_render):
        fake_roadtrip = MagicMock()
        mock_bus.handle.return_value = fake_roadtrip
        mock_render.return_value = "rendered_edit_form"

        with self.app.test_request_context("/admin/roadtrips/rt-123/edit"):
            g.user = self.admin_user
            res = edit_roadtrip_admin_page("rt-123")

            self.assertEqual(res, "rendered_edit_form")
            mock_bus.handle.assert_called_once_with(GetRoadTripByIDCommand(id="rt-123"))
            mock_render.assert_called_once_with(
                "admin/roadtrip_form.html",
                mode="edit",
                roadtrip=fake_roadtrip,
            )

    @patch("app.adapters.inputs.admin_views.render_template")
    @patch("app.adapters.inputs.admin_views.message_bus")
    def test_users_admin_page(self, mock_bus, mock_render):
        mock_bus.handle.return_value = ([self.admin_user], 1, 1)
        mock_render.return_value = "rendered_users"

        with self.app.test_request_context("/admin/users?page=1"):
            g.user = self.admin_user
            res = users_admin_page()

            self.assertEqual(res, "rendered_users")
            mock_bus.handle.assert_called_once_with(
                GetAllUsersPaginatedCommand(current_page=1, limit=10)
            )
            mock_render.assert_called_once_with(
                "admin/users.html",
                users=[self.admin_user],
                current_page=1,
                max_pages=1,
            )

