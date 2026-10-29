from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

import pytest

from app.adapters.outputs.datasources.postgresql_repositories.postgresql_roadtrip_repository import (
    PostgreSQLRoadTripRepository,
)
from app.domain.exceptions.bad_request_exception import BadRequestException
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.models.coordinates_model import CoordinatesModel
from app.domain.models.roadtrip_model import RoadTripModel


class TestPostgreSQLRoadTripRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.repo = PostgreSQLRoadTripRepository(self.mock_session)
        self.sample_roadtrip = RoadTripModel(
            id="018f1234-5678-7000-8000-000000000099",
            display_name="Rodada Oriente",
            start_at=datetime(2026, 12, 15, 7, 0, 0),
            start_coordinates=CoordinatesModel(latitude=6.24, longitude=-75.58, name="Medellín"),
            end_coordinates=CoordinatesModel(latitude=6.15, longitude=-75.37, name="Rionegro"),
            created_by="018f1234-5678-7000-8000-000000000001",
            updated_by="018f1234-5678-7000-8000-000000000001",
        )

    def test_count(self):
        self.mock_session.scalar.return_value = 7
        self.assertEqual(self.repo.count(), 7)

        self.mock_session.scalar.return_value = None
        self.assertEqual(self.repo.count(), 0)

    def test_count_upcoming(self):
        self.mock_session.scalar.return_value = 3
        self.assertEqual(self.repo.count_upcoming(), 3)

    def test_get_by_id_found(self):
        mock_entity = MagicMock()
        mock_entity.to_model.return_value = self.sample_roadtrip
        self.mock_session.scalar.return_value = mock_entity

        result = self.repo.get_by_id("018f1234-5678-7000-8000-000000000099")
        self.assertEqual(result, self.sample_roadtrip)

    def test_get_by_id_not_found_raises_exception(self):
        self.mock_session.scalar.return_value = None
        with pytest.raises(NotFoundException, match="Roadtrip not found"):
            self.repo.get_by_id("018f1234-5678-7000-8000-000000000099")

    def test_get_many(self):
        mock_entity = MagicMock()
        mock_entity.to_model.return_value = self.sample_roadtrip
        self.mock_session.scalars.return_value.all.return_value = [mock_entity]

        result = self.repo.get_many(limit=5, offset=0)
        self.assertEqual(result, [self.sample_roadtrip])

    @patch("app.adapters.outputs.datasources.postgresql_repositories.postgresql_roadtrip_repository.RoadTripEntity")
    def test_save(self, mock_entity_cls):
        mock_entity = MagicMock()
        mock_entity.to_model.return_value = self.sample_roadtrip
        mock_entity_cls.from_model.return_value = mock_entity

        result = self.repo.save(self.sample_roadtrip)

        self.assertEqual(result, self.sample_roadtrip)
        self.mock_session.add.assert_called_once_with(mock_entity)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(mock_entity)

    def test_update_success(self):
        self.repo.update(self.sample_roadtrip)
        self.mock_session.query.assert_called_once()
        self.mock_session.commit.assert_called_once()

    def test_update_without_id_raises_not_found(self):
        rt = self.sample_roadtrip.model_copy(update={"id": None})
        with pytest.raises(NotFoundException, match="Roadtrip not found"):
            self.repo.update(rt)

    def test_update_without_updated_by_raises_bad_request(self):
        rt = self.sample_roadtrip.model_copy(update={"updated_by": None})
        with pytest.raises(BadRequestException, match="Roadtrip update requires an actor"):
            self.repo.update(rt)

