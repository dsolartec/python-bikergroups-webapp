from datetime import datetime
from unittest.mock import MagicMock
import pytest

from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.coordinates_model import CoordinatesModel
from app.domain.models.permission_model import PermissionModel
from app.domain.models.roadtrip_model import RoadTripModel
from app.domain.models.user_model import UserModel


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.__exit__.return_value = None
    return uow


@pytest.fixture
def mock_container(mock_uow):
    container = MagicMock()
    container.unit_of_work.return_value = mock_uow
    return container


@pytest.fixture
def mock_message_bus():
    return MagicMock()


@pytest.fixture
def sample_user():
    return UserModel(
        id="018f1234-5678-7000-8000-000000000001",
        phone="3001234567",
        password="hashed_password",
        display_name="Test Rider",
        created_at=datetime(2026, 1, 1, 10, 0, 0),
        updated_at=datetime(2026, 1, 1, 10, 0, 0),
        permissions=[
            PermissionModel(
                id="018f1234-5678-7000-8000-000000000010",
                name=PermissionEnum.CAN_CREATE_ROADTRIP,
            )
        ],
    )


@pytest.fixture
def sample_roadtrip():
    return RoadTripModel(
        id="018f1234-5678-7000-8000-000000000099",
        display_name="Rodada a Guatapé",
        start_at=datetime(2026, 12, 15, 7, 0, 0),
        start_coordinates=CoordinatesModel(
            latitude=6.2442,
            longitude=-75.5812,
            name="Medellín",
        ),
        end_coordinates=CoordinatesModel(
            latitude=6.2328,
            longitude=-75.1636,
            name="Guatapé",
        ),
        created_at=datetime(2026, 1, 1, 10, 0, 0),
        created_by="018f1234-5678-7000-8000-000000000001",
        updated_at=datetime(2026, 1, 1, 10, 0, 0),
        updated_by="018f1234-5678-7000-8000-000000000001",
    )

