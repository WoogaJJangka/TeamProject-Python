class Player:  # 플레이어 클래스 정의
    def __init__(self, turn, color):  # 플레이어 생성자 (초기 설정)
        self.color = color              # 플레이어 색상 (예: 'red', 'blue', 'green', 'yellow')
        self.turn = turn                # 플레이어 턴 번호 (순서 지정용)
        self.money = 5000               # 초기 자금 (게임 시작 시 보유 금액)
        self.position = 0              # 현재 위치 (타일 인덱스, 시작은 0)
        self.properties = []           # 소유한 타일 목록 (빈 리스트로 시작)
        self.is_bankrupt = False       # 파산 여부 (초기에는 파산하지 않음)

    def move(self, steps, board_size=20):
        # 플레이어 이동 메서드: 현재 위치에서 주어진 칸 수만큼 이동
        # board_size는 전체 타일 수, 기본값은 20
        self.position = (self.position + steps) % board_size
        # 현재 위치에 steps를 더한 뒤 보드 크기만큼 나눈 나머지를 위치로 설정 (보드 순환)

    def pay(self, amount):
        # 플레이어가 금액을 지불하는 메서드
        self.money -= amount  # 보유 금액에서 지불할 금액만큼 차감
        if self.money >= 0:
            # 잔액이 0 이상이면 정상 지불
            return True
        elif self.money < 0:
            # 잔액이 0보다 작아졌다면 지불 실패 (파산 가능성)
            return False