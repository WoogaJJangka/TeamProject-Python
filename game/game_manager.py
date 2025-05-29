import random
from tile import Tile # 타일 클레스를 불러옴
from player import Player # 플레이어 클래스를 불러옴

# 게임 매니저 클래스
class GameManager:
    def __init__(self): # 플레이어 와 타일을 셋팅
        self.players = [
            Player(1, 'red'), Player(2, 'blue'),
            Player(3, 'green'), Player(4, 'yellow')
        ]
        self.current_player_index = 0 # 현제 플레이어 인덱스
        self.tiles = [Tile(f"땅 {i+1}", i) for i in range(20)] # 20개의 타일을 생성 ('땅 1', 0)
        self.board_size = len(self.tiles) # 보드 사이즈

    def roll_dice(self): # 주사위 굴리기기
        d1, d2 = random.randint(1, 6), random.randint(1, 6) # 주사위 2개를 굴림
        if d1 == d2: # 만약 주사위 2개가 같으면
            return d1 + d2 + self.roll_dice() # 다시 주사위를 굴림
        return d1 + d2

    def get_current_player_color(self): # 현제 플레이어 색깔 반환
        return self.players[self.current_player_index].color

    def get_board_matrix(self): # 보드 매트릭스인데 이건 이제 승모가 알아서 하실 거니까 무시하시고
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