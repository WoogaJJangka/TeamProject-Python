import random
from game.tile import Tile
from game.player import Player

class GameManager:
    def __init__(self):
        self.players = [
            Player(1, 'red'), Player(2, 'blue'),
            Player(3, 'green'), Player(4, 'yellow')
        ]
        self.current_player_index = 0
        self.tiles = [Tile(f"땅 {i+1}", i) for i in range(20)]
        self.board_size = len(self.tiles)

    def roll_dice(self):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        steps = d1 + d2
        extra = (d1 == d2)
        return steps, extra

    def get_current_player_color(self):
        return self.players[self.current_player_index].color

    def get_board_matrix(self):
        board = [[None for _ in range(6)] for _ in range(6)]
        coords = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
            (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
            (5, 4), (5, 3), (5, 2), (5, 1), (5, 0),
            (4, 0), (3, 0), (2, 0), (1, 0)
        ]
        event_pos = [(0, 0), (0, 5), (5, 5), (5, 0)]

        for i, (x, y) in enumerate(coords):
            if (x, y) in event_pos:
                board[x][y] = {
                    "type": "event", "name": "이벤트",
                    "owner": None, "upgrade": 0, "players": []
                }
            else:
                tile = self.tiles[i]
                board[x][y] = {
                    "type": "land", "name": tile.name,
                    "owner": tile.owner.color if tile.owner else None,
                    "upgrade": tile.upgrade_level,
                    "players": []
                }

        for p in self.players:
            if not p.is_bankrupt:
                if p.position < len(coords):
                    x, y = coords[p.position]
                    board[x][y]["players"].append(p.color)

        return board