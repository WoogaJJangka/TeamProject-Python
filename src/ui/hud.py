"""
HUD (Heads-Up Display) - 콘솔, 버튼, 플레이어 정보
"""
import pygame
from config import settings
from src.core.constants import COLORS

class HUD:
    """게임 정보 표시 (콘솔 메시지, 버튼 등)"""
    
    @staticmethod
    def draw_console(background: pygame.Surface, messages: list, font: pygame.font.Font):
        """
        콘솔 메시지 그리기
        
        Args:
            background: 그릴 서피스
            messages: 메시지 리스트 (최신순)
            font: 폰트
        """
        start_y = background.get_height() // 2 - (settings.CONSOLE_MAX_LINES * 20)
        box_width = settings.CONSOLE_BOX_WIDTH
        box_height = settings.CONSOLE_MAX_LINES * 80
        
        # 배경 박스
        s = pygame.Surface((box_width, box_height))
        s.fill(COLORS['white'])
        background.blit(s, (40, start_y - 2))
        
        # 메시지 줄바꿈 처리
        max_chars = 22
        y = start_y + (settings.CONSOLE_MAX_LINES - 1) * 20
        all_lines = []
        
        for msg in messages:
            lines = [msg[i:i+max_chars] for i in range(0, len(msg), max_chars)]
            all_lines.extend(lines[::-1])
        
        all_lines = all_lines[:settings.CONSOLE_MAX_LINES]
        
        # 메시지 출력 (아래부터 위로)
        for line in all_lines:
            rendered = font.render(line, True, (30, 30, 30))
            background.blit(rendered, (45, y))
            y -= 20
            if y < start_y - 20:
                break
    
    @staticmethod
    def draw_dialog(background: pygame.Surface, question_text: str, buttons: list,
                    font: pygame.font.Font):
        """
        구매/업그레이드 대화 그리기
        
        Args:
            background: 그릴 서피스
            question_text: 질문 텍스트
            buttons: 버튼 리스트
            font: 폰트
        """
        question = font.render(question_text, True, COLORS['black'])
        background.blit(question, (60, background.get_height() - 180))
        
        for btn in buttons:
            btn.draw(background)
    
    @staticmethod
    def draw_players_info(background: pygame.Surface, game_manager):
        """
        플레이어 정보 그리기
        """
        for idx, player in enumerate(game_manager.players):
            player.draw_info(background, pos=(1200, 50 + idx * 160))
