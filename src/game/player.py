"""
플레이어 클래스 (Player Model)
"""
import pygame
from config import settings
from src.core.constants import COLORS, PLAYER_COLORS_LIGHT, FONTS_PATH
from src.core.resource_loader import resource_loader

class Player:
    """게임 플레이어 모델"""
    
    def __init__(self, turn: int, color: str):
        """
        플레이어 초기화
        
        Args:
            turn (int): 플레이어 턴 번호 (0-3)
            color (str): 플레이어 색상 ('red', 'blue', 'green', 'yellow')
        """
        self.color = color
        self.turn = turn
        self.money = settings.INITIAL_MONEY
        self.position = settings.INITIAL_POSITION
        self.properties = []  # 소유한 타일 목록
        self.is_bankrupt = False
        self.stop_turns = 0  # 무주도 등으로 인한 이동 불가 턴
        self.piece_image = None  # UI용 말 이미지
    
    def move(self, steps: int, board_size: int = settings.BOARD_SIZE):
        """
        플레이어 이동
        
        Args:
            steps (int): 이동할 칸 수
            board_size (int): 보드 크기 (기본값: 20)
        """
        self.position = (self.position + steps) % board_size
    
    def pay(self, amount: int) -> bool:
        """
        금액 지불
        
        Returns:
            bool: 지불 성공 여부
        """
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def add_money(self, amount: int):
        """
        금액 획득
        
        Args:
            amount (int): 받을 금액
        """
        self.money += amount
    
    def draw_info(self, background: pygame.Surface, pos: tuple = (1250, 50)):
        """
        플레이어 정보 화면에 그리기
        
        Args:
            background (pygame.Surface): 그릴 대상 서피스
            pos (tuple): (x, y) 위치
        """
        box_width, box_height = settings.PLAYER_INFO_WIDTH, settings.PLAYER_INFO_HEIGHT
        
        # 배경 박스
        pygame.draw.rect(background, COLORS['white'], (pos[0], pos[1], box_width, box_height), 0, border_radius=10)
        pygame.draw.rect(background, COLORS['black'], (pos[0], pos[1], box_width, box_height), 2, border_radius=10)
        
        # 폰트 로드
        font = resource_loader.load_font(
            FONTS_PATH + '/font.ttf' if FONTS_PATH else None,
            28
        )
        
        # 플레이어 이름 (색상)
        player_color_rgb = PLAYER_COLORS_LIGHT.get(self.color, COLORS['white'])
        np_text = f"P{self.turn+1} : "
        color_text = self.color
        
        np_rendered = font.render(np_text, True, COLORS['black'])
        color_rendered = font.render(color_text, True, PLAYER_COLORS_LIGHT.get(self.color, COLORS['black']))
        
        y = pos[1] + 15
        background.blit(np_rendered, (pos[0] + 15, y))
        background.blit(color_rendered, (pos[0] + 15 + np_rendered.get_width(), y))
        
        # 정보 텍스트
        y += 32
        lines = [
            f"소지금: {self.money} 원",
            f"보유 건물: {len(self.properties)}개"
        ]
        
        for line in lines:
            rendered = font.render(line, True, COLORS['black'])
            background.blit(rendered, (pos[0] + 15, y))
            y += 32
    
    def __repr__(self):
        return f"Player({self.color}, money={self.money}, pos={self.position})"
