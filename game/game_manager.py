import random
import game.player as player# 플레이어 클래스를 불러옴
import game.tile_info as tile_info # 타일 정보를 불러옴
# 게임 매니저 클래스
class GameManager:
    
    def __init__(self): # 플레이어 와 타일을 셋팅
        self.players = [
            player.Player(0, 'red'), player.Player(1, 'blue'),
            player.Player(2, 'green'), player.Player(3, 'yellow')
        ]
        self.current_player_index = 0 # 현제 플레이어 인덱스
        
        self.tiles = [tile_info.Tile(f"땅 {i+1}", i) for i in range(20)] # 20개의 타일을 생성 (0, 19)

    def get_current_player_color(self): # 현제 플레이어 색깔 반환
    
        return self.players[self.current_player_index].color

    def get_current_player(self): # 현제 플레이어 객체 반환
        return self.players[self.current_player_index]
    
    def turn_over(self): # 턴을 넘기는 메서드
        self.current_player_index = (self.current_player_index + 1) % 4
        return self.current_player_index
    
    def buy_tile(self, tile_index, player_index): # 타일 구메 메서드
        player = self.players[player_index]
        tile = self.tiles[tile_index] 
        
         # 플레이어 돈 확인
        if player.pay(tile.price):
            tile.owner = player
            player.properties.append(tile)
            return True, f"{player.color} 플레이어가 {tile.name}을(를) 구매했습니다."
        else:
            return False, f"{player.color} 플레이어는 {tile.name}을(를) 구매할 돈이 부족합니다."

    def upgrade_tile(self, tile_index, player_index):
        player = self.players[player_index]  # 인덱스로 플레이어 객체 접근
        tile = self.tiles[tile_index]

        # 소유 여부 확인
        if tile.owner != player:
            return False, f"{tile.name}은(는) {player.color} 플레이어의 소유가 아닙니다."

        # 업그레이드 한도 확인
        if tile.upgrade_level >= 2:
            return False, f"{tile.name}은(는) 이미 최대 업그레이드 상태입니다."

        # 비용 계산
        cost = 500 if tile.upgrade_level == 0 else 1000

        # 돈 지불 시도
        if player.pay(cost):
            tile.upgrade()
            return True, f"{tile.name}을 업그레이드 했습니다! (현재 LV{tile.upgrade_level})"
        else:
            return False, f"{player.color} 플레이어는 업그레이드 비용 ₩{cost}가 부족합니다."

    def pay_toll(self, tile_index, player_index):
        player = self.players[player_index]
        tile = self.tiles[tile_index]

        # 땅에 주인이 없거나, 자기 자신이라면 통행료 없음
        if tile.owner is None or tile.owner == player:
            return False, "통행료를 지불할 필요가 없습니다."

        toll = tile.toll

        # 플레이어가 돈을 지불할 수 있는지 확인
        if player.pay(toll):
            tile.owner.money += toll
            return True, f"{player.color} 플레이어가 {tile.owner.color} 플레이어에게 통행료 ₩{toll}을 지불했습니다."
        else:
            # 돈이 부족해도 pay()는 음수로 만들고 False 반환함
            return False, f"{player.color} 플레이어는 통행료 ₩{toll}을 낼 수 없습니다. (잔액 부족)"
        
    def tile_event(self, tile_index, player_index):
        player = self.players[player_index]
        tile = self.tiles[tile_index]

        # 타일 소유 여부 확인
        if tile.owner is None:
            # 타일이 비어있으면 구매 가능
            return self.buy_tile(tile_index, player_index)
        elif tile.owner == player:
            # 자기 소유 타일이면 업그레이드 가능
            return self.upgrade_tile(tile_index, player_index)
        else:
            # 다른 플레이어 소유 타일이면 통행료 지불
            return self.pay_toll(tile_index, player_index)
