import unittest
import pytest

from app.adapters.outputs.libraries.utils import Utils


class TestUtils(unittest.TestCase):
    def test_is_allowed_image_extension_valid_jpeg(self):
        self.assertTrue(Utils.is_allowed_image_extension("photo.jpeg"))
        self.assertTrue(Utils.is_allowed_image_extension("my.trip.JPEG"))

    def test_is_allowed_image_extension_invalid(self):
        self.assertFalse(Utils.is_allowed_image_extension("photo.png"))
        self.assertFalse(Utils.is_allowed_image_extension("photo.jpg"))
        self.assertFalse(Utils.is_allowed_image_extension("noextension"))
        self.assertFalse(Utils.is_allowed_image_extension(""))


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("roadtrip.jpeg", True),
        ("ROADTRIP.JPEG", True),
        ("roadtrip.png", False),
        ("roadtrip", False),
    ],
)
def test_utils_parametrized(filename, expected):
    assert Utils.is_allowed_image_extension(filename) is expected

