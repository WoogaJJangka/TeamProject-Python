import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from game.game_manager import GameManager


class GameManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = GameManager()
        self.player = self.manager.players[0]
        self.tile = self.manager.tiles[1]

    def test_buy_tile_updates_owner_and_money(self):
        success, _ = self.manager.buy_tile(1, 0)

        self.assertTrue(success)
        self.assertIs(self.tile.owner, self.player)
        self.assertEqual(self.player.money, 3700)
        self.assertIn(self.tile, self.player.properties)

    def test_upgrade_tile_updates_level_and_toll(self):
        self.manager.buy_tile(1, 0)
        original_toll = self.tile.toll

        success, _ = self.manager.upgrade_tile(1, 0)

        self.assertTrue(success)
        self.assertEqual(self.tile.upgrade_level, 1)
        self.assertGreater(self.tile.toll, original_toll)
        self.assertEqual(self.player.money, 3200)

    def test_player_move_wraps_at_board_size(self):
        self.player.move(21, self.manager.board_size)

        self.assertEqual(self.player.position, 1)

    def test_turn_cycles_through_configured_players(self):
        for _ in range(len(self.manager.players)):
            self.manager.turn_over()

        self.assertEqual(self.manager.current_player_index, 0)

    def test_winner_is_player_with_five_more_properties(self):
        for tile in self.manager.tiles[1:6]:
            tile.owner = self.player
            self.player.properties.append(tile)

        winner, reason = self.manager.check_winner()

        self.assertIs(winner, self.player)
        self.assertEqual(reason, "property")


if __name__ == "__main__":
    unittest.main()
