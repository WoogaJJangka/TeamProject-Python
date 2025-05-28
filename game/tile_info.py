class Tile: # 타일 클래스
    def __init__(self, name, position): # 타일 기본 설정
        self.name = name # 타일 이름
        self.position = position # 타일 위치
        self.owner = None # 타일 소유자
        self.price = 1000 # 타일 가격
        self.toll = int(self.price * 1.3) # 타일 세금
        self.upgrade_level = 0 # 업그레이드 레벨

    def upgrade(self): # 업그레이드 메서드
        # 업그레이드 레벨에 따라 통행료 증가
        if self.upgrade_level == 0:
            self.upgrade_level = 1
            self.toll = int((self.price + 500) * 1.8)
        elif self.upgrade_level == 1:
            self.upgrade_level = 2
            self.toll = int((self.price + 500 + 1000) * 2.2)

    def get_total_value(self): # 총 비용
        # 총 투자 금액 반환
        if self.upgrade_level == 0:
            return self.price
        elif self.upgrade_level == 1:
            return self.price + 500
        else:
            return self.price + 500 + 1000