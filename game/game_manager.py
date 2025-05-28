import game.player as player# 플레이어 클래스를 불러옴
import game.tile_info as tile_info # 타일 정보를 불러옴
# 게임 매니저 클래스
class GameManager:
    ''' 게임의 상태를 관리하는 클래스 '''
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
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
         # 플레이어 돈 확인
        if player.pay(tile.price):
            tile.owner = player
            player.properties.append(tile)
            return True, f"{player.color} 플레이어가 {tile.name}을(를) 구매했습니다."
        else:
            return False, f"{player.color} 플레이어는 {tile.name}을(를) 구매할 돈이 부족합니다."

    def upgrade_tile(self, tile_index, player_index):
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        

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
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
        # 땅에 주인이 없거나, 자기 자신이라면 통행료 없음
        if tile.owner is None or tile.owner == player:
            return False, "통행료를 지불할 필요가 없습니다."

        toll = tile.toll

        # 플레이어가 돈을 지불할 수 있는지 확인
        if player.pay(toll):
            tile.owner.money += toll
            return True, f"{player.color} 플레이어가 {tile.owner.color} 플레이어에게 통행료 ₩{toll}을 지불했습니다."
        else:
            is_bankrupt, log = self.check_and_handle_bankruptcy(player_index, toll) # 통행료를 지불 할 수 있는지 확인
            if is_bankrupt: # 파산 상태라면
                return False, log # False와 로그를 반환
            else:
                return True, log + [f"{player.color} 플레이어가 {tile.owner.color} 플레이어에게 통행료 ₩{toll}을 지불했습니다."]
        
    def tile_event(self, tile_index, player_index): # 일반 타일을 받았을 때 실행되는 메서드
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
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
        
    def sell_properties_until_enough(self, player_index, amount_needed):
        player = self.players[player_index]
        log = []

        while player.properties and player.money < amount_needed:
            tile = player.properties.pop(0)  # 가장 먼저 산 땅부터
            spent = tile.get_total_value()  # 구매 + 업그레이드 금액
            refund = int(spent * 0.7) # 70% 환불

            player.money += refund
            tile.owner = None
            tile.upgrade_level = 0

            log.append(f"{player.color} 플레이어가 {tile.name}을 팔고 ₩{refund}를 받았습니다.")

        return log

    def check_and_handle_bankruptcy(self, player_index, amount_needed):
        player = self.players[player_index]

        # 1. 시도: 가진 돈으로는 부족 → 땅을 팔아서 마련
        if player.money < amount_needed and player.properties:
            log = self.sell_properties_until_enough(player_index, amount_needed)
        else:
            log = []

        # 2. 다시 확인: 충분한 돈이 모였는지
        if player.money >= amount_needed:
            player.pay(amount_needed)
            return False, log + [f"{player.color} 플레이어가 통행료 ₩{amount_needed}를 납부했습니다."]
        else:
            # 3. 여전히 부족하면 파산 처리
            player.is_bankrupt = True
            log.append(f"{player.color} 플레이어는 파산했습니다.")
            return True, log
    
    def teleport_player(self, player_index, destination_index): # 플레이어를 순간이동시키는 메서드
        player = self.players[player_index]
        # 이동 처리
        player.position = destination_index

        return True, f"{player.color} 플레이어가 {destination_index}번 타일로 순간이동했습니다."
