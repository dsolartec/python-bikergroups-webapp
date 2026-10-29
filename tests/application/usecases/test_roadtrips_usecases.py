from datetime import datetime
from io import BytesIO
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask
import pytest
from werkzeug.datastructures import FileStorage

from app.application.usecases.roadtrips_usecases import RoadTripsUseCases
from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.commands.delete_one_roadtrip_command import DeleteOneRoadTripCommand
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_roadtrip_by_id_command import GetRoadTripByIDCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.exceptions.bad_request_exception import BadRequestException
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.models.coordinates_model import CoordinatesModel
from app.domain.models.roadtrip_model import RoadTripModel


class TestRoadTripsUseCases(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.mock_uow = MagicMock()
        self.mock_uow.__enter__.return_value = self.mock_uow

        self.mock_container = MagicMock()
        self.mock_container.unit_of_work.return_value = self.mock_uow
        self.mock_bus = MagicMock()

        self.roadtrip = RoadTripModel(
            id="018f1234-5678-7000-8000-000000000099",
            display_name="Rodada a Jardín",
            start_at=datetime(2026, 12, 1, 7, 0, 0),
            start_coordinates=CoordinatesModel(latitude=6.24, longitude=-75.58, name="Medellín"),
            end_coordinates=CoordinatesModel(latitude=5.59, longitude=-75.81, name="Jardín"),
            created_at=datetime(2026, 1, 1, 10, 0, 0),
            created_by="018f1234-5678-7000-8000-000000000001",
            updated_at=datetime(2026, 1, 1, 10, 0, 0),
            updated_by="018f1234-5678-7000-8000-000000000001",
        )

    def test_create_one_saves_roadtrip_and_audit_log(self):
        self.mock_uow.roadtrip_repository.save.return_value = self.roadtrip

        cmd = CreateOneRoadTripCommand(
            display_name="Rodada a Jardín",
            start_at=datetime(2026, 12, 1, 7, 0, 0),
            start_coordinates=self.roadtrip.start_coordinates,
            end_coordinates=self.roadtrip.end_coordinates,
            actor_id="018f1234-5678-7000-8000-000000000001",
        )
        result = RoadTripsUseCases.create_one(cmd, self.mock_bus, self.mock_container)

        self.assertEqual(result, self.roadtrip)
        self.mock_uow.roadtrip_repository.save.assert_called_once()
        self.mock_uow.audit_log_repository.save.assert_called_once()
        saved_log = self.mock_uow.audit_log_repository.save.call_args[0][0]
        self.assertEqual(saved_log.action, AuditLogActionEnum.ROADTRIP_CREATED)

    def test_delete_one_executes_without_error(self):
        cmd = DeleteOneRoadTripCommand(actor_id="actor-1", roadtrip_id="rt-1")
        result = RoadTripsUseCases.delete_one(cmd, self.mock_bus, self.mock_container)
        self.assertIsNone(result)

    def test_get_all_paginated_success(self):
        self.mock_uow.roadtrip_repository.count.return_value = 7
        self.mock_uow.roadtrip_repository.get_many.return_value = [self.roadtrip]

        cmd = GetAllRoadtripsPaginatedCommand(current_page=2, limit=5)
        items, total, max_pages = RoadTripsUseCases.get_all_paginated(
            cmd, self.mock_bus, self.mock_container
        )

        self.assertEqual(items, [self.roadtrip])
        self.assertEqual(total, 7)
        self.assertEqual(max_pages, 2)
        self.mock_uow.roadtrip_repository.get_many.assert_called_once_with(limit=5, offset=5)

    def test_get_all_paginated_invalid_page_raises_bad_request(self):
        cmd = GetAllRoadtripsPaginatedCommand(current_page=0, limit=5)
        with pytest.raises(BadRequestException, match="Current page is invalid"):
            RoadTripsUseCases.get_all_paginated(cmd, self.mock_bus, self.mock_container)

    def test_get_all_paginated_page_beyond_max_returns_empty_list(self):
        self.mock_uow.roadtrip_repository.count.return_value = 3
        cmd = GetAllRoadtripsPaginatedCommand(current_page=5, limit=5)

        items, total, max_pages = RoadTripsUseCases.get_all_paginated(
            cmd, self.mock_bus, self.mock_container
        )
        self.assertEqual(items, [])
        self.assertEqual(total, 3)
        self.assertEqual(max_pages, 1)

    def test_get_by_id_found_and_not_found(self):
        self.mock_uow.roadtrip_repository.get_by_id.return_value = self.roadtrip
        cmd = GetRoadTripByIDCommand(id=self.roadtrip.id)
        self.assertEqual(
            RoadTripsUseCases.get_by_id(cmd, self.mock_bus, self.mock_container),
            self.roadtrip,
        )

        self.mock_uow.roadtrip_repository.get_by_id.side_effect = NotFoundException("Not found")
        self.assertIsNone(RoadTripsUseCases.get_by_id(cmd, self.mock_bus, self.mock_container))

    def test_update_photo_missing_file_raises_bad_request(self):
        cmd = UpdateRoadTripPhotoCommand(actor_id="actor-1", roadtrip_id="rt-1")
        with self.app.test_request_context("/upload", method="POST", data={}):
            with pytest.raises(BadRequestException, match="You're not uploading a valid image"):
                RoadTripsUseCases.update_photo(cmd, self.mock_bus, self.mock_container)

    def test_update_photo_invalid_extension_raises_bad_request(self):
        cmd = UpdateRoadTripPhotoCommand(actor_id="actor-1", roadtrip_id="rt-1")
        file_storage = FileStorage(stream=BytesIO(b"fake"), filename="photo.png")
        with self.app.test_request_context(
            "/upload", method="POST", data={"file": file_storage}
        ):
            with pytest.raises(BadRequestException, match="You're not uploading a valid image"):
                RoadTripsUseCases.update_photo(cmd, self.mock_bus, self.mock_container)

    @patch.object(FileStorage, "save")
    def test_update_photo_valid_jpeg_saves_and_logs(self, mock_file_save):
        self.mock_uow.roadtrip_repository.get_by_id.return_value = self.roadtrip
        cmd = UpdateRoadTripPhotoCommand(
            actor_id="018f1234-5678-7000-8000-000000000002",
            roadtrip_id=self.roadtrip.id,
        )
        file_storage = FileStorage(stream=BytesIO(b"jpeg-bytes"), filename="cover.jpeg")

        with self.app.test_request_context(
            "/upload", method="POST", data={"file": file_storage}
        ):
            RoadTripsUseCases.update_photo(cmd, self.mock_bus, self.mock_container)

        mock_file_save.assert_called_once_with(
            f"./app/static/images/roadtrips/{self.roadtrip.id}.jpeg"
        )
        self.mock_uow.roadtrip_repository.update.assert_called_once()
        self.mock_uow.audit_log_repository.save.assert_called_once()
        saved_log = self.mock_uow.audit_log_repository.save.call_args[0][0]
        self.assertEqual(saved_log.action, AuditLogActionEnum.ROADTRIP_PHOTO_UPDATED)

