from app.domain.commands.get_admin_stats_command import GetAdminStatsCommand
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class AdminUseCases:
    @staticmethod
    def get_stats(
            cmd: GetAdminStatsCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[int, int]:
        with container.unit_of_work() as uow:
            total_upcoming_roadtrips = uow.roadtrip_repository.count_upcoming()
            total_users = uow.user_repository.count()

            return total_upcoming_roadtrips, total_users
