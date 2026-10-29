import unittest
from unittest.mock import MagicMock

from app.application.usecases.admin_usecases import AdminUseCases
from app.domain.commands.get_admin_stats_command import GetAdminStatsCommand


class TestAdminUseCases(unittest.TestCase):
    def test_get_stats_returns_upcoming_roadtrips_and_total_users(self):
        mock_uow = MagicMock()
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.roadtrip_repository.count_upcoming.return_value = 4
        mock_uow.user_repository.count.return_value = 25

        mock_container = MagicMock()
        mock_container.unit_of_work.return_value = mock_uow
        mock_bus = MagicMock()

        result = AdminUseCases.get_stats(
            GetAdminStatsCommand(),
            mock_bus,
            mock_container,
        )

        self.assertEqual(result, (4, 25))
        mock_uow.roadtrip_repository.count_upcoming.assert_called_once()
        mock_uow.user_repository.count.assert_called_once()

