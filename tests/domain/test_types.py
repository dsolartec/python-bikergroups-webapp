from datetime import datetime
import unittest

from pydantic import BaseModel

from app.domain.types import FormattedDateTime, T


class _SampleDateModel(BaseModel):
    timestamp: FormattedDateTime


class TestDomainTypes(unittest.TestCase):
    def test_formatted_datetime_serializes_to_expected_string(self):
        dt = datetime(2026, 10, 29, 15, 30, 45)
        model = _SampleDateModel(timestamp=dt)

        dumped = model.model_dump()
        self.assertEqual(dumped["timestamp"], "2026-10-29 15:30:45")

    def test_typevar_t_is_defined(self):
        self.assertEqual(T.__name__, "T")

