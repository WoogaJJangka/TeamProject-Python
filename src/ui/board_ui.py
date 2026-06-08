"""
보드판 UI (Board Rendering)
"""
import pygame
from src.core.constants import COLORS

class BoardUI:
    """보드판 시각화"""
    
    @staticmethod
    def draw_board(background: pygame.Surface):
        """
        보드판 기본 구조 그리기
        (3개의 중첩 정사각형 + 격자 + 타일 구분선)
        """
        # 큰 사각형 3개 그리기
        pygame.draw.rect(background, COLORS['black'], (500, 250, 500, 500), 3)
        pygame.draw.rect(background, COLORS['black'], (450, 200, 600, 600), 3)
        pygame.draw.rect(background, COLORS['black'], (350, 100, 800, 800), 3)
        
        # 이벤트 지역에 넘어간 선 지우기 (흰색 직사각형 덮기)
        pygame.draw.rect(background, COLORS['white'], (350, 100, 153, 153), 99)
        pygame.draw.rect(background, COLORS['white'], (997, 100, 153, 153), 99)
        pygame.draw.rect(background, COLORS['white'], (350, 747, 153, 153), 99)
        pygame.draw.rect(background, COLORS['white'], (997, 747, 153, 153), 99)
        
        # 이벤트 지역 다시 그리기
        pygame.draw.rect(background, COLORS['black'], (350, 100, 153, 153), 3)
        pygame.draw.rect(background, COLORS['black'], (997, 100, 153, 153), 3)
        pygame.draw.rect(background, COLORS['black'], (350, 747, 153, 153), 3)
        pygame.draw.rect(background, COLORS['black'], (997, 747, 153, 153), 3)
        
        # 지역 나누는 선 그리기 (가로칸)
        for j in range(2):
            for i in range(3):
                pygame.draw.line(background, COLORS['black'], 
                               (625 + 125 * i, 250 + 647 * j),
                               (625 + 125 * i, 100 + 650 * j), 3)
        
        # 지역 나누는 선 그리기 (세로칸)
        for j in range(2):
            for i in range(3):
                pygame.draw.line(background, COLORS['black'],
                               (350 + 650 * j, 375 + 125 * i),
                               (500 + 647 * j, 375 + 125 * i), 3)
    
    @staticmethod
    def draw_center_text(background: pygame.Surface, font: pygame.font.Font):
        """보드 중앙에 '조선 유람' 텍스트 그리기"""
        rendered1 = font.render("조선", True, COLORS['black'])
        rendered2 = font.render("유람", True, COLORS['black'])
        background.blit(rendered1, (695, 440))
        background.blit(rendered2, (695, 505))
    
    @staticmethod
    def draw_tiles(background: pygame.Surface, tiles: list, mouse_pos: tuple):
        """
        모든 타일 그리기
        
        Args:
            background: 그릴 서피스
            tiles: 타일 리스트
            mouse_pos: 마우스 위치
        """
        # 하이라이트 타일 결정
        highlight_tile = None
        for tile in tiles:
            if tile.visual.rect.collidepoint(mouse_pos):
                highlight_tile = tile
                break
        
        # 타일 그리기
        for tile in tiles:
            tile.draw_owner_box(background)  # 소유자 박스
            is_highlight = tile is highlight_tile
            tile.visual.draw(background, tile.name, highlight=is_highlight)
        
        # 타일 정보 표시
        if highlight_tile:
            highlight_tile.draw_info(background, pos=(50, 50))
    
    @staticmethod
    def draw_player_pieces(background: pygame.Surface, game_manager, current_player_index: int):
        """
        플레이어 말 그리기
        """
        for idx, player in enumerate(game_manager.players):
            if not hasattr(player, 'piece_image') or player.piece_image is None:
                continue
            
            tile = game_manager.tiles[player.position]
            pos = tile.player_positions[player.turn]
            pos = (pos[0] + 10, pos[1] + 10)
            
            img_rect = player.piece_image.get_rect(center=(int(pos[0]), int(pos[1])))
            background.blit(player.piece_image, img_rect)
        
        # 플레이어 정보창 테두리
        for idx in range(len(game_manager.players)):
            pygame.draw.rect(background, COLORS['white'], (1195, 45 + idx * 160, 260, 160), 4)
        
        # 현재 턴 플레이어 테두리 강조
        idx = current_player_index
        pygame.draw.rect(background, COLORS['red'], (1195, 45 + idx * 160, 260, 160), 4)
