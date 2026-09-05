from typing import Callable, Type

from app.application.usecases.auth_usecases import AuthUseCases
from app.application.usecases.roadtrips_usecases import RoadTripsUseCases
from app.domain.commands.base_command import BaseCommand
from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.commands.refresh_command import RefreshTokenCommand
from app.domain.commands.signin_command import SignInCommand
from app.domain.commands.signup_command import SignUpCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand


COMMAND_HANDLERS: dict[Type[BaseCommand], Callable] = {
    # Auth usecases
    RefreshTokenCommand: AuthUseCases.refresh,
    SignInCommand: AuthUseCases.signin,
    SignUpCommand: AuthUseCases.signup,

    # Roadtrips usecases
    CreateOneRoadTripCommand: RoadTripsUseCases.create_one,
    UpdateRoadTripPhotoCommand: RoadTripsUseCases.update_photo,
}
