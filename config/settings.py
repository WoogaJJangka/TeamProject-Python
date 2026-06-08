"""
게임 설정 (Game Configuration)
"""

# 윈도우 설정
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000
WINDOW_TITLE = "조선 유람"
FPS = 120

# 게임 보드 설정
BOARD_SIZE = 20  # 타일 개수
INITIAL_MONEY = 5000  # 초기 자금
INITIAL_POSITION = 0  # 시작 위치

# 출도(Go) 보너스
GO_BONUS = 2000

# 무주도(Jail) 설정
JAIL_STOP_TURNS = 2  # 무주도에서 멈추는 턴 수

# 업그레이드 비용
UPGRADE_COSTS = {
    0: 500,    # LV0 -> LV1: 500원
    1: 1000,   # LV1 -> LV2: 1000원
}

# 통행료 계산 배수
TOLL_MULTIPLIERS = {
    0: 1.3,    # LV0: 가격의 1.3배
    1: 1.8,    # LV1: (가격+500)의 1.8배
    2: 2.2,    # LV2: (가격+1500)의 2.2배
}

# 건물 매각 환급율
PROPERTY_SELL_REFUND_RATE = 0.7  # 원가의 70%

# 땅 개수로 인한 우승 조건
PROPERTY_LEAD_FOR_VICTORY = 5  # 5개 이상 차이나면 우승

# 디버그 모드
DEBUG = False
