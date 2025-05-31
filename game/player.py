import pygame

FONT_PATH = "board_set/font.ttf" # 글꼴 위치

class Player:  # 플레이어 클래스 정의
    def __init__(self, turn, color):  # 플레이어 생성자 (초기 설정)
        self.color = color              # 플레이어 색상 (예: 'red', 'blue', 'green', 'yellow')
        self.turn = turn                # 플레이어 턴 번호 (순서 지정용)
        self.money = 5000               # 초기 자금 (게임 시작 시 보유 금액)
        self.position = 0              # 현재 위치 (타일 인덱스, 시작은 0)
        self.properties = []           # 소유한 타일 목록 (빈 리스트로 시작)
        self.is_bankrupt = False       # 파산 여부 (초기에는 파산하지 않음)
        self.stop_turns = 0            # 무주도 등 이동불가 턴 수 (쉬운 단어)

    def move(self, steps, board_size=20):
        # 플레이어 이동 메서드: 현재 위치에서 주어진 칸 수만큼 이동
        # board_size는 전체 타일 수, 기본값은 20
        self.position = (self.position + steps) % board_size
        # 현재 위치에 steps를 더한 뒤 보드 크기만큼 나눈 나머지를 위치로 설정 (보드 순환)

    def pay(self, amount):
        # 플레이어가 금액을 지불하는 메서드
        if self.money >= amount: # 잔액이 지불 비용 이상이면 정상 지불
            self.money -= amount  # 보유 금액에서 지불할 금액만큼 차감
            return True
        elif self.money < amount: # 잔액이 지불 비용보다 작아졌다면 지불 실패 (파산 가능성)
            return False
    
    def draw_info(self, background, pos=(1250, 50)):
        # pos 위치에 네모 박스와 정보 출력
        box_width, box_height = 250, 150
        pygame.draw.rect(background, (255,255,255), (pos[0], pos[1], box_width, box_height), 0, border_radius=10)
        pygame.draw.rect(background, (0,0,0), (pos[0], pos[1], box_width, box_height), 2, border_radius=10)

        font = pygame.font.Font(FONT_PATH, 28)
        # 이름 색상만 진하게(원래 색상)
        color_map = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 128, 0),
            'yellow': (220, 220, 0)
        }
        player_color = color_map.get(self.color, (0,0,0))
        # 첫 줄: P1, P2, ... : color (color만 진한 색)
        np_text = f"P{self.turn+1} : "
        color_text = self.color
        np_rendered = font.render(np_text, True, (0,0,0))
        color_rendered = font.render(color_text, True, player_color)
        y = pos[1] + 15
        background.blit(np_rendered, (pos[0] + 15, y))
        background.blit(color_rendered, (pos[0] + 15 + np_rendered.get_width(), y))
        y += 32
        # 나머지 정보
        lines = [
            f"소지금: {self.money} 원",
            f"보유 건물: {len(self.properties)}개"
        ]
        for line in lines:
            rendered = font.render(line, True, (0,0,0))
            background.blit(rendered, (pos[0] + 15, y))
            y += 32  # 줄 간격
