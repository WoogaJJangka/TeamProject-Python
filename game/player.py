class Player: # 플레이어 클래스
    def __init__(self, turn, color): # 플레이어 기본 설정
        self.color = color  # 플레이어 색깔 (red, blue, green, yellow)
        self.turn = turn # 플레이어 턴
        self.money = 5000 # 시작 돈
        self.position = 0 # 시작 위치
        self.properties = [] # 소유한 타일
        self.is_bankrupt = False # 파산 여부

    def move(self, steps, board_size = 20): # 이동 메서드
        self.position = (self.position + steps) % board_size # 현재 위치에서 주사위의 합을 더한 후 보드 사이즈로 나눈 나머지로 이동

    def pay(self, amount): # 돈 지불
        self.money -= amount # 현재 돈에서 지불금을 빼기
        if self.money >= 0: # 만약 현재 돈이 0 이상이면 True를 리턴
            return True
        elif self.money < 0:
            return False # 만약 현재 돈이 0보다 작으면 False를 리턴