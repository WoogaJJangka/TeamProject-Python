"""
UI 상태 관리 (Encapsulates global UI state)
"""
import pygame
from config import settings
from src.core.constants import COLORS

class Button:
    """UI 버튼"""
    
    def __init__(self, rect: tuple, text: str, font: pygame.font.Font, 
                 color=(200, 200, 200), text_color=(0, 0, 0)):
        """
        버튼 초기화
        
        Args:
            rect (tuple): (x, y, width, height)
            text (str): 버튼 텍스트
            font (pygame.font.Font): 폰트
            color: 버튼 배경색
            text_color: 텍스트 색상
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
    
    def draw(self, surface: pygame.Surface):
        """버튼 그리기"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, COLORS['dark_gray'], self.rect, 2)
        rendered = self.font.render(self.text, True, self.text_color)
        text_rect = rendered.get_rect(center=self.rect.center)
        surface.blit(rendered, text_rect)
    
    def is_clicked(self, pos: tuple) -> bool:
        """마우스 클릭 감지"""
        return self.rect.collidepoint(pos)


class UIState:
    """UI 전체 상태 관리 (전역 변수 제거)"""
    
    def __init__(self):
        """UI 상태 초기화"""
        # 구매 상태
        self.ask_buy = False
        self.buy_tile_index = None
        self.buy_player_index = None
        self.buy_buttons = []
        
        # 업그레이드 상태
        self.ask_upgrade = False
        self.upgrade_tile_index = None
        self.upgrade_player_index = None
        self.upgrade_buttons = []
        
        # 콘솔 메시지
        self.console_messages = []
        
        # 순간이동 상태
        self.is_teleporting = False
        self.teleport_player_index = None
    
    def start_buy_dialog(self, tile_index: int, player_index: int, font: pygame.font.Font, 
                         screen_height: int):
        """구매 대화 시작"""
        self.ask_buy = True
        self.buy_tile_index = tile_index
        self.buy_player_index = player_index
        self.buy_buttons = [
            Button((60, screen_height - 140, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT), 
                   "예", font),
            Button((160, screen_height - 140, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT), 
                   "아니요", font)
        ]
    
    def end_buy_dialog(self):
        """구매 대화 종료"""
        self.ask_buy = False
        self.buy_tile_index = None
        self.buy_player_index = None
        self.buy_buttons = []
    
    def start_upgrade_dialog(self, tile_index: int, player_index: int, font: pygame.font.Font,
                             screen_height: int):
        """업그레이드 대화 시작"""
        self.ask_upgrade = True
        self.upgrade_tile_index = tile_index
        self.upgrade_player_index = player_index
        self.upgrade_buttons = [
            Button((60, screen_height - 140, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT), 
                   "예", font),
            Button((160, screen_height - 140, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT), 
                   "아니요", font)
        ]
    
    def end_upgrade_dialog(self):
        """업그레이드 대화 종료"""
        self.ask_upgrade = False
        self.upgrade_tile_index = None
        self.upgrade_player_index = None
        self.upgrade_buttons = []
    
    def start_teleport(self, player_index: int):
        """순간이동 시작"""
        self.is_teleporting = True
        self.teleport_player_index = player_index
    
    def end_teleport(self):
        """순간이동 종료"""
        self.is_teleporting = False
        self.teleport_player_index = None
    
    def add_message(self, msg):
        """메시지 추가"""
        if isinstance(msg, list):
            for m in msg:
                self.console_messages.insert(0, str(m))
                print(str(m))
        else:
            self.console_messages.insert(0, str(msg))
            print(str(msg))
        
        # 최대 줄 수 초과 시 오래된 메시지 제거
        while len(self.console_messages) > settings.CONSOLE_MAX_LINES:
            self.console_messages.pop()
    
    def clear_messages(self):
        """모든 메시지 제거"""
        self.console_messages.clear()
