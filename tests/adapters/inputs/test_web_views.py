from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask, g, get_flashed_messages, session

from app.adapters.inputs.web_views import (
    landing_page,
    load_logged_user_from_session,
    roadtrip_page,
    roadtrips_page,
    signin_page,
    signout_page,
    signup_page,
    web_views,
)
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_roadtrip_by_id_command import GetRoadTripByIDCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.phone_already_exists_exception import PhoneAlreadyExistsException
from app.domain.exceptions.wrong_credentials_exception import WrongCredentialsException
from app.domain.models.permission_model import PermissionModel
from app.domain.models.user_model import UserModel


class TestWebViews(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "test-secret"
        self.app.register_blueprint(web_views)

        self.user = UserModel(
            id="018f1234-5678-7000-8000-000000000001",
            phone="3001234567",
            display_name="Test User",
            created_at=datetime(2026, 1, 1, 10, 0, 0),
            updated_at=datetime(2026, 1, 1, 10, 0, 0),
            permissions=[
                PermissionModel(
                    id="018f1234-5678-7000-8000-000000000010",
                    name=PermissionEnum.CAN_CREATE_ROADTRIP,
                )
            ],
        )

    def test_load_logged_user_from_session_unlogged(self):
        with self.app.test_request_context("/"):
            load_logged_user_from_session()
            self.assertFalse(g.in_hk)
            self.assertFalse(g.can_hk)
            self.assertIsNone(g.user)

    @patch("app.adapters.inputs.web_views.message_bus")
    def test_load_logged_user_from_session_logged(self, mock_bus):
        mock_bus.handle.return_value = self.user

        with self.app.test_request_context("/"):
            session["user_id"] = self.user.id
            load_logged_user_from_session()

            self.assertFalse(g.in_hk)
            self.assertTrue(g.can_hk)
            self.assertEqual(g.user, self.user)

    @patch("app.adapters.inputs.web_views.message_bus")
    def test_load_logged_user_from_session_not_found(self, mock_bus):
        mock_bus.handle.side_effect = NotFoundException("User not found")

        with self.app.test_request_context("/"):
            session["user_id"] = "missing"
            load_logged_user_from_session()

            self.assertFalse(g.can_hk)
            self.assertIsNone(g.user)
            self.assertNotIn("user_id", session)

    @patch("app.adapters.inputs.web_views.render_template")
    @patch("app.adapters.inputs.web_views.message_bus")
    def test_landing_page(self, mock_bus, mock_render):
        rt1, rt2 = MagicMock(), MagicMock()
        mock_bus.handle.return_value = ([rt1, rt2], 2, 1)
        mock_render.return_value = "rendered_landing"

        with self.app.test_request_context("/"):
            res = landing_page()

            self.assertEqual(res, "rendered_landing")
            mock_bus.handle.assert_called_once_with(
                GetAllRoadtripsPaginatedCommand(current_page=1, limit=5)
            )
            mock_render.assert_called_once_with(
                "index.html",
                recent_roadtrips={"first": rt1, "rest": [rt2]},
                roadtrips_count=2,
            )

    @patch("app.adapters.inputs.web_views.render_template")
    @patch("app.adapters.inputs.web_views.message_bus")
    def test_roadtrips_page(self, mock_bus, mock_render):
        rt1 = MagicMock()
        mock_bus.handle.return_value = ([rt1], 1, 1)
        mock_render.return_value = "rendered_roadtrips"

        with self.app.test_request_context("/roadtrips?page=1"):
            res = roadtrips_page()

            self.assertEqual(res, "rendered_roadtrips")
            mock_bus.handle.assert_called_once_with(
                GetAllRoadtripsPaginatedCommand(current_page=1, limit=6)
            )
            mock_render.assert_called_once_with(
                "roadtrips.html",
                page_roadtrips=[rt1],
                total_roadtrips_count=1,
                current_page=1,
                max_pages=1,
            )

    @patch("app.adapters.inputs.web_views.render_template")
    @patch("app.adapters.inputs.web_views.message_bus")
    def test_roadtrip_page(self, mock_bus, mock_render):
        rt = MagicMock()
        mock_bus.handle.return_value = rt
        mock_render.return_value = "rendered_roadtrip"

        with self.app.test_request_context("/roadtrip/rt-1"):
            res = roadtrip_page("rt-1")

            self.assertEqual(res, "rendered_roadtrip")
            mock_bus.handle.assert_called_once_with(GetRoadTripByIDCommand(id="rt-1"))
            mock_render.assert_called_once_with("roadtrip.html", roadtrip=rt)

    @patch("app.adapters.inputs.web_views.message_bus")
    def test_signin_page_post_success(self, mock_bus):
        mock_bus.handle.return_value = self.user

        with self.app.test_request_context(
            "/login",
            method="POST",
            data={"phone": "3001234567", "password": "Password123"},
        ):
            g.user = None
            response = signin_page()

            self.assertEqual(response.status_code, 302)
            self.assertEqual(session["user_id"], self.user.id)
            mock_bus.handle.assert_called_once_with(
                SignInCommand(password="Password123", phone="3001234567")
            )

    @patch("app.adapters.inputs.web_views.render_template")
    @patch("app.adapters.inputs.web_views.message_bus")
    def test_signin_page_post_wrong_credentials(self, mock_bus, mock_render):
        mock_bus.handle.side_effect = WrongCredentialsException()
        mock_render.return_value = "rendered_auth"

        with self.app.test_request_context(
            "/login",
            method="POST",
            data={"phone": "3001234567", "password": "WrongPassword1"},
        ):
            g.user = None
            res = signin_page()

            self.assertEqual(res, "rendered_auth")
            flashed = get_flashed_messages(with_categories=True)
            self.assertIn(
                ("signin.error", "El número de teléfono o la contraseña no son válidos"),
                flashed,
            )

    @patch("app.adapters.inputs.web_views.message_bus")
    def test_signup_page_post_success(self, mock_bus):
        mock_bus.handle.return_value = self.user

        with self.app.test_request_context(
            "/register",
            method="POST",
            data={
                "display_name": "Rider Test",
                "phone": "3001234567",
                "password": "Password123",
                "confirm_password": "Password123",
            },
        ):
            g.user = None
            response = signup_page()

            self.assertEqual(response.status_code, 302)
            self.assertEqual(session["user_id"], self.user.id)
            mock_bus.handle.assert_called_once_with(
                SignUpCommand(
                    display_name="Rider Test",
                    password="Password123",
                    phone="3001234567",
                )
            )

    @patch("app.adapters.inputs.web_views.render_template")
    @patch("app.adapters.inputs.web_views.message_bus")
    def test_signup_page_validation_errors(self, mock_bus, mock_render):
        mock_render.return_value = "rendered_auth"

        with self.app.test_request_context(
            "/register",
            method="POST",
            data={
                "display_name": "abc",
                "phone": "200123",
                "password": "short",
                "confirm_password": "other",
            },
        ):
            g.user = None
            res = signup_page()

            self.assertEqual(res, "rendered_auth")
            mock_bus.handle.assert_not_called()
            categories = [cat for cat, _ in get_flashed_messages(with_categories=True)]
            self.assertIn("signup.display_name.error", categories)
            self.assertIn("signup.phone.error", categories)
            self.assertIn("signup.password.error", categories)
            self.assertIn("signup.confirm_password.error", categories)

    @patch("app.adapters.inputs.web_views.render_template")
    @patch("app.adapters.inputs.web_views.message_bus")
    def test_signup_page_phone_already_exists(self, mock_bus, mock_render):
        mock_bus.handle.side_effect = PhoneAlreadyExistsException()
        mock_render.return_value = "rendered_auth"

        with self.app.test_request_context(
            "/register",
            method="POST",
            data={
                "display_name": "Rider Test",
                "phone": "3001234567",
                "password": "Password123",
                "confirm_password": "Password123",
            },
        ):
            g.user = None
            res = signup_page()

            self.assertEqual(res, "rendered_auth")
            flashed = get_flashed_messages(with_categories=True)
            self.assertIn(("signup.phone.error", "El número de teléfono ya está en uso"), flashed)

    def test_signout_page_clears_session_and_redirects(self):
        with self.app.test_request_context("/logout"):
            g.user = self.user
            session["user_id"] = self.user.id

            response = signout_page()

            self.assertEqual(response.status_code, 302)
            self.assertNotIn("user_id", session)

