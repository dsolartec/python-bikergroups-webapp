from typing import Callable, Type

from app.application.usecases.admin_usecases import AdminUseCases
from app.application.usecases.auth_usecases import AuthUseCases
from app.application.usecases.roadtrips_usecases import RoadTripsUseCases
from app.application.usecases.users_usecases import UsersUseCases
from app.domain.commands.base_command import BaseCommand
from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.commands.get_admin_stats_command import GetAdminStatsCommand
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.get_all_users_paginated_command import GetAllUsersPaginatedCommand
from app.domain.commands.get_roadtrip_by_id_command import GetRoadTripByIDCommand
from app.domain.commands.get_user_by_id_command import GetUserByIDCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand


COMMAND_HANDLERS: dict[Type[BaseCommand], Callable] = {
    # Auth usecases
    SignInCommand: AuthUseCases.signin,
    SignUpCommand: AuthUseCases.signup,

    # Roadtrips usecases
    CreateOneRoadTripCommand: RoadTripsUseCases.create_one,
    GetAllRoadtripsPaginatedCommand: RoadTripsUseCases.get_all_paginated,
    GetRoadTripByIDCommand: RoadTripsUseCases.get_by_id,
    UpdateRoadTripPhotoCommand: RoadTripsUseCases.update_photo,

    # Users usecases
    GetAllUsersPaginatedCommand: UsersUseCases.get_all_paginated,
    GetUserByIDCommand: UsersUseCases.get_by_id,

    # Admin usecases
    GetAdminStatsCommand: AdminUseCases.get_stats,
}
