from game.tile_info import all_tiles  # 타일 정보와 시각 객체를 포함한 타일 리스트 생성 함수
from game.player import Player  # 플레이어 클래스


class GameManager:
    ''' 게임의 상태를 관리하는 클래스 '''

    def __init__(self):
        # 네 명의 플레이어 초기화
        self.players = [
            Player(0, 'red'), Player(1, 'blue'),
            Player(2, 'green'), Player(3, 'yellow')
        ]
        self.current_player_index = 0  # 현재 턴인 플레이어의 인덱스
        self.tiles = all_tiles()  # 전체 타일 생성 (tile_info에서 시각 타일 포함하여 생성)
        self.board_size = len(self.tiles)  # 보드판의 크기 (타일 수)

    def roll_dice(self):
        ''' 주사위를 굴리는 함수. 더블이 나오면 다시 굴림 '''
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        if d1 == d2:
            return d1 + d2 + self.roll_dice()  # 더블이면 재굴림
        return d1 + d2

    def get_current_player_color(self):
        ''' 현재 플레이어의 색상 반환 '''
        return self.players[self.current_player_index].color

    def get_current_player(self):
        ''' 현재 플레이어 객체 반환 '''
        return self.players[self.current_player_index]

    def turn_over(self):
        ''' 다음 플레이어로 턴 넘기기 '''
        self.current_player_index = (self.current_player_index + 1) % 4
        return self.current_player_index

    def buy_tile(self, tile_index, player_index):
        ''' 타일 구매 시도 함수 '''
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
        if player.pay(tile.price):  # 플레이어가 돈을 낼 수 있으면
            tile.owner = player
            player.properties.append(tile)
            return True, f"{player.color} 플레이어가 {tile.name}을(를) 구매했습니다."
        
        else:
            return False, f"{player.color} 플레이어는 {tile.name}을(를) 구매할 돈이 부족합니다."

    def upgrade_tile(self, tile_index, player_index):
        ''' 소유한 타일 업그레이드 시도 '''
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
        if tile.owner != player:
            return False, f"{tile.name}은(는) {player.color} 플레이어의 소유가 아닙니다."
        
        if tile.upgrade_level >= 2:
            return False, f"{tile.name}은(는) 이미 최대 업그레이드 상태입니다."

        # 업그레이드 비용: LV0 -> 500, LV1 -> 1000
        cost = 500 if tile.upgrade_level == 0 else 1000
        if player.pay(cost):
            tile.upgrade()
            return True, f"{tile.name}을 업그레이드 했습니다! (현재 LV{tile.upgrade_level})"
        else:
            return False, f"{player.color} 플레이어는 업그레이드 비용 ₩{cost}가 부족합니다."

    def pay_toll(self, tile_index, player_index):
        ''' 타일 통행료 지불 처리 '''
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
        # 무주택지 또는 자기 땅이면 통행료 없음
        if tile.owner is None or tile.owner == player:
            return False, "통행료를 지불할 필요가 없습니다."

        toll = tile.toll
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
        ''' 타일에 도착했을 때 발생하는 이벤트 처리 '''
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
        # 타일 소유 여부 확인
        if tile.owner is None:
            return self.buy_tile(tile_index, player_index)
        elif tile.owner == player:
            return self.upgrade_tile(tile_index, player_index)
        else:
            return self.pay_toll(tile_index, player_index)

    def sell_properties_until_enough(self, player_index, amount_needed):
        ''' 목표 금액을 확보할 때까지 플레이어의 부동산을 매각 '''
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
        '''
        플레이어가 돈이 부족한 경우, 부동산 매각 후에도 부족하면 파산 처리
        반환값: (is_bankrupt: bool, log: str 또는 [str])
        '''
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
            # 3. 여전히 돈이 부족하면 파산
            player.is_bankrupt = True
            log.append(f"{player.color} 플레이어는 파산했습니다.")
            return True, log
        
    def teleport_player(self, player_index, destination_index):
        ''' 플레이어를 특정 타일로 순간이동 '''
        player = self.players[player_index]
        # 이동 처리
        player.position = destination_index

        return True, f"{player.color} 플레이어가 {destination_index}번 타일로 순간이동했습니다."
