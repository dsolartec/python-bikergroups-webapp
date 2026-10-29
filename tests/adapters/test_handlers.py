import unittest

from app.adapters.handlers import COMMAND_HANDLERS
from app.application.usecases.admin_usecases import AdminUseCases
from app.application.usecases.auth_usecases import AuthUseCases
from app.application.usecases.roadtrips_usecases import RoadTripsUseCases
from app.application.usecases.users_usecases import UsersUseCases
from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.commands.delete_one_roadtrip_command import DeleteOneRoadTripCommand
from app.domain.commands.get_admin_stats_command import GetAdminStatsCommand
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_all_users_paginated_command import GetAllUsersPaginatedCommand
from app.domain.commands.get_roadtrip_by_id_command import GetRoadTripByIDCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.commands.update_one_roadtrip_command import UpdateOneRoadTripCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand


class TestHandlers(unittest.TestCase):
    def test_command_handlers_mapping(self):
        expected_mapping = {
            SignInCommand: AuthUseCases.signin,
            SignUpCommand: AuthUseCases.signup,
            CreateOneRoadTripCommand: RoadTripsUseCases.create_one,
            DeleteOneRoadTripCommand: RoadTripsUseCases.delete_one,
            GetAllRoadtripsPaginatedCommand: RoadTripsUseCases.get_all_paginated,
            GetRoadTripByIDCommand: RoadTripsUseCases.get_by_id,
            UpdateOneRoadTripCommand: RoadTripsUseCases.update_one,
            UpdateRoadTripPhotoCommand: RoadTripsUseCases.update_photo,
            GetAllUsersPaginatedCommand: UsersUseCases.get_all_paginated,
            GetUserByIDCommand: UsersUseCases.get_by_id,
            GetAdminStatsCommand: AdminUseCases.get_stats,
        }

        self.assertEqual(COMMAND_HANDLERS, expected_mapping)

