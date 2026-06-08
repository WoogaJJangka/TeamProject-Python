"""
타입 정의 및 열거형 (Type Definitions)
"""
from enum import Enum
from typing import Optional, List, Tuple

# ========== 플레이어 관련 타입 ==========
PlayerColor = str  # 'red', 'blue', 'green', 'yellow'
Money = int
Position = int  # 타일 인덱스

class TileType(Enum):
    """타일 종류"""
    NORMAL = "normal"        # 일반 땅
    GO = "go"                # 출도
    JAIL = "jail"            # 무주도
    SCHOOL = "school"        # 학
    DESTINY = "destiny"      # 미정

class GameStatus(Enum):
    """게임 상태"""
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

class TileEventType(Enum):
    """타일 이벤트 타입"""
    NONE = "none"
    PURCHASE_POSSIBLE = "purchase_possible"
    UPGRADE_POSSIBLE = "upgrade_possible"
    PAY_TOLL = "pay_toll"
    OWNED_BY_SELF = "owned_by_self"
    TELEPORT = "teleport"
    STOP = "stop"
    GET_BONUS = "get_bonus"

# ========== 게임 결과 타입 ==========
VictoryReason = str  # 'bankruptcy', 'property'

class GameResult:
    """게임 결과"""
    def __init__(self, winner, reason: VictoryReason, reason_detail: str = ""):
        self.winner = winner
        self.reason = reason
        self.reason_detail = reason_detail
    
    def __repr__(self):
        return f"GameResult(winner={self.winner.color}, reason={self.reason})"
