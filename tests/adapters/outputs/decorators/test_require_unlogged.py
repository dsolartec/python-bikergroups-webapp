from datetime import datetime
import unittest

from flask import Flask, g

from app.adapters.outputs.decorators.require_unlogged import require_unlogged
from app.domain.models.user_model import UserModel


class TestRequireUnlogged(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_allows_when_user_is_unlogged(self):
        @require_unlogged()
        def login_view():
            return "login_page"

        with self.app.test_request_context("/login"):
            g.user = None
            res = login_view()
            self.assertEqual(res, "login_page")

    def test_redirects_when_user_is_logged_in(self):
        @require_unlogged(redirect_to="/dashboard")
        def login_view():
            return "login_page"

        with self.app.test_request_context("/login"):
            g.user = UserModel(
                id="018f1234-5678-7000-8000-000000000001",
                phone="3001234567",
                display_name="User",
                created_at=datetime(2026, 1, 1, 10, 0, 0),
                updated_at=datetime(2026, 1, 1, 10, 0, 0),
            )
            res = login_view()
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "/dashboard")

