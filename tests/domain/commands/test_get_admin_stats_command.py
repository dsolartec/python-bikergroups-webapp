import unittest

from app.domain.commands.base_command import BaseCommand
from app.domain.commands.get_admin_stats_command import GetAdminStatsCommand


class TestGetAdminStatsCommand(unittest.TestCase):
    def test_get_admin_stats_command(self):
        cmd = GetAdminStatsCommand()
        self.assertIsInstance(cmd, BaseCommand)

