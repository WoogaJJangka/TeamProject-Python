"""
게임 매니저 (Game Manager - 순수 로직)
"""
from config import settings
from src.core.types import GameResult, TileEventType
from .tile import all_tiles
from .player import Player

class GameManager:
    """게임 상태 및 규칙을 관리하는 클래스"""
    
    def __init__(self):
        """게임 초기화"""
        self.players = [
            Player(0, 'red'), Player(1, 'blue'),
            Player(2, 'green'), Player(3, 'yellow')
        ]
        self.current_player_index = 0
        self.tiles = all_tiles()
        self.board_size = len(self.tiles)
    
    def get_current_player(self):
        """현재 차례의 플레이어 반환"""
        return self.players[self.current_player_index]
    
    def get_current_player_color(self) -> str:
        """현재 플레이어 색상 반환"""
        return self.players[self.current_player_index].color
    
    def turn_over(self):
        """다음 플레이어로 턴 이동"""
        self.current_player_index = (self.current_player_index + 1) % 4
        return self.current_player_index
    
    def buy_tile(self, tile_index: int, player_index: int) -> tuple:
        """
        타일 구매 처리
        
        Returns:
            (success: bool, message: str)
        """
        special_tiles = [0, 5, 10, 15]
        
        if tile_index in special_tiles:
            return False, f"{self.tiles[tile_index].name} 칸은 구매할 수 없습니다."
        
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
        if player.money < tile.price:
            return False, f"{player.color} 플레이어는 {tile.name}을(를) 구매할 돈이 부족합니다."
        
        player.pay(tile.price)
        tile.owner = player
        player.properties.append(tile)
        
        return True, f"{player.color} 플레이어가 {tile.name}을(를) 구매했습니다."
    
    def upgrade_tile(self, tile_index: int, player_index: int) -> tuple:
        """
        타일 업그레이드
        
        Returns:
            (success: bool, message: str)
        """
        player = self.players[player_index]
        tile = self.tiles[tile_index]
        
        if tile.owner != player:
            return False, f"{tile.name}은(는) {player.color} 플레이어의 소유가 아닙니다."
        
        if tile.upgrade_level >= 2:
            return False, f"{tile.name}은(는) 이미 최대 업그레이드 상태입니다."
        
        cost = settings.UPGRADE_COSTS.get(tile.upgrade_level, 500)
        
        if not player.pay(cost):
            return False, f"{player.color} 플레이어는 업그레이드 비용 ₩{cost}가 부족합니다."
        
        tile.upgrade()
        return True, f"{tile.name}을 업그레이드 했습니다! (현재 LV{tile.upgrade_level})"
    
    def pay_toll(self, tile_index: int, player_index: int) -> tuple:
        """
        통행료 지불 처리
        
        Returns:
            (success: bool, messages: list)
        """
        player = self.players[player_index]
        tile = self.tiles[tile_index]
        logs = []
        
        # 무주택지 또는 자기 땅이면 통행료 없음
        if tile.owner is None or tile.owner == player:
            return False, ["통행료를 지불할 필요가 없습니다."]
        
        toll = tile.toll
        
        # 1. 돈이 부족하면 건물 매각 시도
        if player.money < toll and player.properties:
            logs = self.sell_properties_until_enough(player_index, toll)
        
        # 2. 매각 후에도 돈이 부족하면 파산
        if player.money >= toll:
            player.pay(toll)
            tile.owner.add_money(toll)
            logs.append(f"{player.color} 플레이어가 {tile.owner.color} 플레이어에게 통행료 ₩{toll}을 지불했습니다.")
            return True, logs
        else:
            # 가진 돈 전부 지급
            paid = max(0, player.money)
            tile.owner.add_money(paid)
            player.money = 0
            player.is_bankrupt = True
            logs.append(f"{player.color} 플레이어가 가진 돈 {paid}원을 모두 {tile.owner.color} 플레이어에게 주고 파산했습니다.")
            return False, logs
    
    def tile_event(self, tile_index: int, player_index: int) -> tuple:
        """
        타일 도착 이벤트 반환 (자동 처리 하지 않음)
        
        Returns:
            (event_type: TileEventType, data: dict)
        """
        tile = self.tiles[tile_index]
        player = self.players[player_index]
        
        # 특수 타일 처리는 app.py에서 수행
        if tile_index in [0, 5, 10, 15]:
            if tile_index == 0:  # 출도
                return TileEventType.GET_BONUS, {"amount": settings.GO_BONUS}
            elif tile_index == 5:  # 미정
                return TileEventType.NONE, {}
            elif tile_index == 10:  # 무주도
                return TileEventType.STOP, {"turns": settings.JAIL_STOP_TURNS}
            elif tile_index == 15:  # 학
                return TileEventType.TELEPORT, {}
        
        # 일반 타일
        if tile.owner is None and tile.price > 0:
            if player.money < tile.price:
                return TileEventType.NONE, {}
            return TileEventType.PURCHASE_POSSIBLE, {"tile_index": tile_index}
        elif tile.owner == player and tile.price > 0 and tile.upgrade_level < 2:
            return TileEventType.UPGRADE_POSSIBLE, {"tile_index": tile_index}
        elif tile.owner and tile.owner != player and tile.price > 0:
            return TileEventType.PAY_TOLL, {"tile_index": tile_index}
        
        return TileEventType.NONE, {}
    
    def sell_properties_until_enough(self, player_index: int, amount_needed: int) -> list:
        """
        목표 금액 확보할 때까지 건물 매각
        
        Returns:
            logs: 매각 로그 리스트
        """
        player = self.players[player_index]
        logs = []
        
        while player.properties and player.money < amount_needed:
            tile = player.properties.pop(0)
            refund = int(tile.get_total_value() * settings.PROPERTY_SELL_REFUND_RATE)
            player.add_money(refund)
            tile.owner = None
            tile.upgrade_level = 0
            logs.append(f"{player.color} 플레이어가 {tile.name}을 팔고 ₩{refund}를 받았습니다.")
        
        return logs
    
    def teleport_player(self, player_index: int, destination_tile_index: int) -> tuple:
        """
        플레이어 순간이동
        
        Returns:
            (success: bool, message: str)
        """
        if destination_tile_index == 15:  # 학 타일로는 이동 불가
            return False, "학 타일로는 순간이동할 수 없습니다."
        
        player = self.players[player_index]
        player.position = destination_tile_index
        return True, f"{player.color} 플레이어가 {destination_tile_index}번 타일로 순간이동했습니다."
    
    def check_winner(self) -> tuple:
        """
        우승자 확인
        
        Returns:
            (winner: Player or None, reason: str or None)
        """
        alive_players = [p for p in self.players if not p.is_bankrupt]
        
        # 파산으로 인한 우승 (1명만 남음)
        if len(alive_players) == 1:
            return alive_players[0], 'bankruptcy'
        
        # 땅 개수로 인한 우승
        if len(alive_players) >= 2:
            property_counts = [(p, len(p.properties)) for p in alive_players]
            property_counts.sort(key=lambda x: x[1], reverse=True)
            
            if property_counts[0][1] - property_counts[1][1] >= settings.PROPERTY_LEAD_FOR_VICTORY:
                return property_counts[0][0], 'property'
        
        return None, None
