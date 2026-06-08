"""
메인 렌더러 (Main Rendering Loop)
"""
import pygame
from config import settings
from src.core.constants import COLORS
from .board_ui import BoardUI
from .hud import HUD

class Renderer:
    """게임 렌더링 담당"""
    
    def __init__(self, screen: pygame.Surface, game_manager, ui_state, dice_ui):
        """
        렌더러 초기화
        
        Args:
            screen (pygame.Surface): Pygame 화면
            game_manager: GameManager 인스턴스
            ui_state: UIState 인스턴스
            dice_ui: DiceUI 인스턴스
        """
        self.screen = screen
        self.game_manager = game_manager
        self.ui_state = ui_state
        self.dice_ui = dice_ui
        self.font_console = pygame.font.SysFont('arial', 16)
        self.font_dialog = pygame.font.SysFont('arial', 18)
    
    def render(self, mouse_pos: tuple):
        """
        현재 프레임 렌더링
        
        Args:
            mouse_pos (tuple): 마우스 위치 (x, y)
        """
        # 배경 초기화
        self.screen.fill(COLORS['white'])
        
        # 보드판 그리기
        BoardUI.draw_board(self.screen)
        BoardUI.draw_center_text(self.screen, pygame.font.SysFont('arial', 60))
        BoardUI.draw_tiles(self.screen, self.game_manager.tiles, mouse_pos)
        BoardUI.draw_player_pieces(self.screen, self.game_manager, 
                                   self.game_manager.current_player_index)
        
        # 플레이어 정보
        HUD.draw_players_info(self.screen, self.game_manager)
        
        # 콘솔 메시지
        HUD.draw_console(self.screen, self.ui_state.console_messages, self.font_console)
        
        # 구매 대화
        if self.ui_state.ask_buy:
            HUD.draw_dialog(self.screen, "땅을 구매하겠습니까?", 
                          self.ui_state.buy_buttons, self.font_dialog)
        
        # 업그레이드 대화
        if self.ui_state.ask_upgrade:
            HUD.draw_dialog(self.screen, "땅을 업그레이드 하시겠습니까?",
                          self.ui_state.upgrade_buttons, self.font_dialog)
        
        # 화면 업데이트
        pygame.display.update()
    
    def render_teleport_selection(self, mouse_pos: tuple):
        """
        순간이동 타일 선택 렌더링
        """
        self.screen.fill(COLORS['white'])
        
        # 보드판
        BoardUI.draw_board(self.screen)
        BoardUI.draw_center_text(self.screen, pygame.font.SysFont('arial', 60))
        
        # 하이라이트 타일
        highlight_tile = None
        for tile in self.game_manager.tiles:
            if tile.visual.rect.collidepoint(mouse_pos):
                highlight_tile = tile
                break
        
        for tile in self.game_manager.tiles:
            tile.draw_owner_box(self.screen)
            is_highlight = tile is highlight_tile
            tile.visual.draw(self.screen, tile.name, highlight=is_highlight)
        
        if highlight_tile:
            highlight_tile.draw_info(self.screen, pos=(50, 50))
        
        # 플레이어 정보
        for idx, p in enumerate(self.game_manager.players):
            p.draw_info(self.screen, pos=(1200, 50 + idx * 160))
        
        pygame.display.update()
