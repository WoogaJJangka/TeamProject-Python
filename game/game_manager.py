from game.tile_info import all_tiles  # 타일 정보와 시각 객체를 포함한 타일 리스트 생성 함수
from game.player import Player  # 플레이어 클래스

# 게임의 상태를 관리하는 클래스
class GameManager:
    ''' 게임의 상태를 관리하는 클래스 '''

    def __init__(self):
        # 네 명의 플레이어 초기화 (항상 인덱스 0~3, 색상 순서 고정)
        self.players = [
            Player(0, 'red'), Player(1, 'blue'),
            Player(2, 'green'), Player(3, 'yellow')
        ]
        self.current_player_index = 0  # 현재 턴인 플레이어의 인덱스
        self.tiles = all_tiles()  # 전체 타일 생성 (tile_info에서 시각 타일 포함하여 생성)
        self.board_size = len(self.tiles)  # 보드판의 크기 (타일 수)

    def roll_dice(self):
        ''' 주사위를 굴리는 함수. 더블이 나오면 다시 굴림 '''
        d1, d2 = random.randint(1, 6), random.randint(1, 6)  # 두 개의 주사위 굴림
        if d1 == d2:
            return d1 + d2 + self.roll_dice()  # 더블이면 재굴림
        return d1 + d2

    def get_current_player_color(self):
        ''' 현재 플레이어의 색상 반환 '''
        return self.players[self.current_player_index].color

    def get_current_player(self):
        # 항상 current_player_index 기준으로 반환
        return self.players[self.current_player_index]

    def turn_over(self):
        # 다음 플레이어로 턴 넘기기 (0→1→2→3→0)
        self.current_player_index = (self.current_player_index + 1) % 4
        return self.current_player_index

    def buy_tile(self, tile_index, player_index):
        ''' 타일 구매 시도 함수 '''
        special_tile_names = ["출도", "학", "무주도", "미정"]  # 특수 타일 이름 목록
        tile = self.tiles[tile_index]  # 현재 타일 객체
        if tile.name in special_tile_names:
            msg = f"{tile.name} 칸은 구매할 수 없습니다."
            print(msg)
            return False, msg  # 특수 타일은 구매 불가
        player = self.players[player_index]  # 현재 플레이어 객체
        # 돈이 부족하면 구매 불가, 돈 차감도 하지 않음
        if player.money < tile.price:
            msg = f"{player.color} 플레이어는 {tile.name}을(를) 구매할 돈이 부족합니다."
            print(msg)
            return False, msg
        player.pay(tile.price)  # 타일 가격만큼 돈 차감
        tile.owner = player  # 타일 소유자 지정
        player.properties.append(tile)  # 플레이어 소유 목록에 추가
        msg = f"{player.color} 플레이어가 {tile.name}을(를) 구매했습니다."
        print(msg)
        return True, msg

    def upgrade_tile(self, tile_index, player_index):
        ''' 소유한 타일 업그레이드 시도 '''
        player = self.players[player_index]  # 현재 플레이어 객체
        tile = self.tiles[tile_index]  # 현재 타일 객체
        if tile.owner != player:
            msg = f"{tile.name}은(는) {player.color} 플레이어의 소유가 아닙니다."
            print(msg)
            return False, msg  # 본인 소유가 아니면 업그레이드 불가
        if tile.upgrade_level >= 2:
            msg = f"{tile.name}은(는) 이미 최대 업그레이드 상태입니다."
            print(msg)
            return False, msg  # 이미 최대 업그레이드

        # 업그레이드 비용: LV0 -> 500, LV1 -> 1000
        cost = 500 if tile.upgrade_level == 0 else 1000
        if player.pay(cost):
            tile.upgrade()  # 타일 업그레이드
            msg = f"{tile.name}을 업그레이드 했습니다! (현재 LV{tile.upgrade_level})"
            print(msg)
            return True, msg
        else:
            msg = f"{player.color} 플레이어는 업그레이드 비용 ₩{cost}가 부족합니다."
            print(msg)
            return False, msg

    def pay_toll(self, tile_index, player_index):
        ''' 타일 통행료 지불 처리 '''
        player = self.players[player_index]  # 현재 플레이어 객체
        tile = self.tiles[tile_index]  # 현재 타일 객체

        # 무주택지 또는 자기 땅이면 통행료 없음
        if tile.owner is None or tile.owner == player:
            msg = "통행료를 지불할 필요가 없습니다."
            print(msg)
            return False, msg

        toll = tile.toll  # 통행료 금액
        # 1. 돈이 부족하면 건물 매각 시도
        if player.money < toll and player.properties:
            log = self.sell_properties_until_enough(player_index, toll)  # 부동산 매각
        else:
            log = []
        # 2. 매각 후에도 돈이 부족하면 가진 돈 전부를 소유주에게 주고 파산
        if player.money >= toll:
            player.pay(toll)  # 통행료 지불
            tile.owner.money += toll  # 소유주에게 돈 지급
            log.append(f"{player.color} 플레이어가 {tile.owner.color} 플레이어에게 통행료 ₩{toll}을 지불했습니다.")
            for msg in log:
                print(msg)
            return True, log
        else:
            paid = max(0, player.money)  # 남은 돈 모두 지급
            tile.owner.money += paid
            player.money -= paid
            player.is_bankrupt = True  # 파산 처리
            log.append(f"{player.color} 플레이어가 가진 돈 {paid}원을 모두 {tile.owner.color} 플레이어에게 주고 파산했습니다.")
            for msg in log:
                print(msg)
            return False, log

    def tile_event(self, tile_index, player_index):
        ''' 타일에 도착했을 때 발생하는 이벤트 처리 '''
        player = self.players[player_index]  # 현재 플레이어 객체
        tile = self.tiles[tile_index]  # 현재 타일 객체
        if tile.owner is None:
            result, msg = self.buy_tile(tile_index, player_index)  # 빈 땅이면 구매 시도
            # buy_tile에서 이미 print 처리
            return result, msg
        elif tile.owner == player:
            # 업그레이드 질문은 main.py에서 버튼으로 처리
            return False, ""
        else:
            result, log = self.pay_toll(tile_index, player_index)  # 타인 소유 땅이면 통행료
            # pay_toll에서 이미 print 처리
            return result, log

    def sell_properties_until_enough(self, player_index, amount_needed):
        ''' 목표 금액을 확보할 때까지 플레이어의 부동산을 매각 '''
        player = self.players[player_index]  # 현재 플레이어 객체
        log = []  # 매각 로그 리스트

        while player.properties and player.money < amount_needed:
            tile = player.properties.pop(0)  # 가장 먼저 산 부동산부터 매각
            spent = tile.get_total_value()  # 투자한 총 금액
            refund = int(spent * 0.7)  # 원가의 70% 반환
            player.money += refund  # 환급금 지급
            tile.owner = None  # 소유권 해제
            tile.upgrade_level = 0  # 업그레이드 초기화
            msg = f"{player.color} 플레이어가 {tile.name}을 팔고 ₩{refund}를 받았습니다."
            log.append(msg)
            print(msg)
        return log

    def check_and_handle_bankruptcy(self, player_index, amount_needed):
        '''
        플레이어가 돈이 부족한 경우, 부동산 매각 후에도 부족하면 파산 처리
        반환값: (is_bankrupt: bool, log: str 또는 [str])
        '''
        player = self.players[player_index]  # 현재 플레이어 객체
        # 1. 시도: 가진 돈으로는 부족 → 땅을 팔아서 마련
        if player.money < amount_needed and player.properties:
            log = self.sell_properties_until_enough(player_index, amount_needed)
        else:
            log = []

        # 2. 다시 확인: 충분한 돈이 모였는지
        if player.money >= amount_needed:
            player.pay(amount_needed)
            # 돈이 음수일 때만 파산 처리 (매각 후 납부 후에도 음수면 파산)
            if player.money < 0:
                player.is_bankrupt = True
                msg = f"{player.color} 플레이어는 파산했습니다."
                log.append(msg)
                print(msg)
                return True, log
            msg = f"{player.color} 플레이어가 통행료 ₩{amount_needed}를 납부했습니다."
            log.append(msg)
            print(msg)
            return False, log
        else:
            # 매각 후에도 납부 불가(돈이 음수)면 파산
            if player.money < 0:
                player.is_bankrupt = True
                msg = f"{player.color} 플레이어는 파산했습니다."
                log.append(msg)
                print(msg)
                return True, log
            # 돈이 0 이상인데도 amount_needed을 못 내는 경우(건물도 없음): 파산 아님, 그냥 못 냄
            msg = f"{player.color} 플레이어는 통행료를 낼 수 없습니다."
            log.append(msg)
            print(msg)
            return False, log

    def check_winner(self):
        # 파산하지 않은 플레이어가 1명 남으면 그 플레이어가 우승
        alive_players = [p for p in self.players if not p.is_bankrupt]
        if len(alive_players) == 1:
            return alive_players[0], 'bankruptcy'
        # 땅 개수 차이로 우승 조건 추가
        property_counts = [(p, len(p.properties)) for p in self.players if not p.is_bankrupt] # 모든 플레이어 중 파산하지 않은 플레이어들 대상
        if len(property_counts) >= 2:
            property_counts.sort(key=lambda x: x[1], reverse=True)
            first, second = property_counts[0][1], property_counts[1][1]
            if first - second >= 5:
                return property_counts[0][0], 'property'
        return None, None

    def teleport_player(self, player_index, destination_tile_index):
        """
        플레이어를 지정한 타일로 순간이동시키는 메서드
        """
        player = self.players[player_index]  # 현재 플레이어 객체
        player.position = destination_tile_index  # 위치 이동
        msg = f"{player.color} 플레이어가 {destination_tile_index}번 타일로 순간이동했습니다."
        print(msg)
        return True, msg