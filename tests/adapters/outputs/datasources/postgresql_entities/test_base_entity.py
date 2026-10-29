import datetime
import unittest

from sqlalchemy import TIMESTAMP

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity


class TestBaseEntity(unittest.TestCase):
    def test_type_annotation_map_contains_datetime_timestamp_with_timezone(self):
        self.assertIn(datetime, BaseEntity.type_annotation_map)
        mapped_type = BaseEntity.type_annotation_map[datetime]
        self.assertIsInstance(mapped_type, TIMESTAMP)
        self.assertTrue(mapped_type.timezone)

