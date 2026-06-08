"""
타일 클래스 및 생성 함수 (Tile Model)
"""
import pygame
from config import settings
from src.core.constants import COLORS, PLAYER_COLORS_LIGHT, FONTS_PATH
from src.core.resource_loader import resource_loader
from src.core.types import TileType

class TileVisual:
    """타일의 시각적 표현"""
    
    def __init__(self, name_size: int, name_position: tuple, rect_info: tuple):
        """
        타일 시각화 객체 초기화
        
        Args:
            name_size (int): 타일 이름 폰트 크기
            name_position (tuple): (x, y) 이름 렌더링 위치
            rect_info (tuple): (x, y, width, height) 타일 영역
        """
        self.name_size = name_size
        self.name_position = name_position
        self.rect = pygame.Rect(rect_info)
    
    def draw(self, background: pygame.Surface, name: str, highlight: bool = False):
        """
        타일을 화면에 그리기
        
        Args:
            background (pygame.Surface): 그릴 대상 서피스
            name (str): 타일 이름
            highlight (bool): 하이라이트 활성화 여부
        """
        color = COLORS['yellow'] if highlight else COLORS['white']
        pygame.draw.rect(background, color, self.rect)
        
        # 텍스트 렌더링
        font = resource_loader.load_font(None, self.name_size)
        rendered = font.render(name, True, COLORS['black'])
        background.blit(rendered, self.name_position)

class Tile:
    """게임 타일"""
    
    def __init__(self, name: str, visual: TileVisual, board_index: int, 
                 tile_type: TileType = TileType.NORMAL, price: int = 1000, 
                 empty_rect: tuple = (0, 0, 0, 0)):
        """
        타일 초기화
        
        Args:
            name (str): 타일 이름
            visual (TileVisual): 시각 객체
            board_index (int): 보드 상 인덱스
            tile_type (TileType): 타일 종류
            price (int): 타일 가격
            empty_rect (tuple): 소유자 표시 네모 (x, y, w, h)
        """
        self.name = name
        self.visual = visual
        self.board_index = board_index
        self.tile_type = tile_type
        self.price = price
        self.owner = None
        self.upgrade_level = 0
        self.toll = self._calculate_toll()
        self.player_positions = self._generate_player_positions()
        self.empty_rect = empty_rect
    
    def _calculate_toll(self) -> int:
        """통행료 계산"""
        multiplier = settings.TOLL_MULTIPLIERS.get(self.upgrade_level, 1.3)
        if self.upgrade_level == 0:
            return int(self.price * multiplier)
        elif self.upgrade_level == 1:
            return int((self.price + 500) * multiplier)
        else:
            return int((self.price + 1500) * multiplier)
    
    def _generate_player_positions(self) -> list:
        """타일 내 플레이어 말 위치 계산 (2x2 그리드)"""
        x, y, w, h = self.visual.rect
        margin = 5
        px, py = x + margin, y + margin
        pw, ph = w - 2 * margin, h - 2 * margin
        return [
            (px + pw * 0.1, py + ph * 0.1),  # 좌상
            (px + pw * 0.6, py + ph * 0.1),  # 우상
            (px + pw * 0.1, py + ph * 0.6),  # 좌하
            (px + pw * 0.6, py + ph * 0.6),  # 우하
        ]
    
    def upgrade(self):
        """타일 업그레이드"""
        if self.upgrade_level < 2:
            self.upgrade_level += 1
            self.toll = self._calculate_toll()
    
    def get_total_value(self) -> int:
        """총 투자 가치 반환"""
        upgrade_cost = settings.UPGRADE_COSTS.get(self.upgrade_level, 0)
        if self.upgrade_level == 0:
            return self.price
        elif self.upgrade_level == 1:
            return self.price + 500
        else:
            return self.price + 1500
    
    def is_clicked(self, mouse_pos: tuple) -> bool:
        """마우스 클릭이 타일 영역에 포함되는지 확인"""
        return self.visual.rect.collidepoint(mouse_pos)
    
    def draw_info(self, background: pygame.Surface, pos: tuple = (50, 50)):
        """타일 정보 화면에 그리기"""
        # 배경 색상 (소유자 색상)
        if self.owner and hasattr(self.owner, 'color'):
            owner_color = PLAYER_COLORS_LIGHT.get(self.owner.color, COLORS['white'])
        else:
            owner_color = COLORS['white']
        
        pygame.draw.rect(background, owner_color, (40, 40, settings.INFO_BOX_WIDTH, settings.INFO_BOX_HEIGHT), 0)
        
        # 텍스트 정보
        font = resource_loader.load_font(None, 28)
        lines = [
            f"위치: {self.name}",
            f"가격: {self.price} 원",
            f"레벨: {self.upgrade_level}",
            f"통행료: {self.toll} 원"
        ]
        
        y = pos[1]
        for line in lines:
            rendered = font.render(line, True, COLORS['black'])
            background.blit(rendered, (pos[0], y))
            y += 35
        
        # 테두리
        pygame.draw.rect(background, COLORS['black'], (40, 40, settings.INFO_BOX_WIDTH, settings.INFO_BOX_HEIGHT), 3)
    
    def draw_owner_box(self, background: pygame.Surface):
        """타일 옆 소유자 색상 네모 그리기"""
        if self.board_index not in [0, 5, 10, 15]:  # 특수 타일 제외
            x, y, w, h = self.empty_rect
            if w > 0 and h > 0:
                owner_color = COLORS['white']
                if self.owner and hasattr(self.owner, 'color'):
                    owner_color = PLAYER_COLORS_LIGHT.get(self.owner.color, COLORS['white'])
                pygame.draw.rect(background, owner_color, (x, y, w, h))


def all_tiles():
    """전체 타일 생성 및 반환"""
    tile_info_list = [
        # (name, name_size, name_pos, rect, tile_type, price, empty_rect)
        ("출도", 45, (1030, 800), (1000, 750, 147, 147), TileType.GO, 0, (0, 0, 0, 0)),
        ("경복궁", 30, (895, 830), (877, 801, 120, 96), TileType.NORMAL, 1300, (877, 750, 120, 47)),
        ("창덕궁", 30, (770, 830), (753, 801, 120, 96), TileType.NORMAL, 1200, (752, 750, 122, 47)),
        ("창경궁", 30, (645, 830), (628, 801, 120, 96), TileType.NORMAL, 1100, (627, 750, 122, 47)),
        ("덕수궁", 30, (520, 830), (503, 801, 120, 96), TileType.NORMAL, 1000, (503, 750, 121, 47)),
        ("미정", 45, (380, 800), (353, 750, 147, 147), TileType.DESTINY, 0, (0, 0, 0, 0)),
        ("남한산성", 25, (355, 670), (353, 627, 96, 120), TileType.NORMAL, 1300, (453, 627, 47, 120)),
        ("흥인지문", 25, (355, 545), (353, 502, 96, 121), TileType.NORMAL, 1200, (453, 502, 47, 122)),
        ("수원화성", 25, (355, 420), (353, 377, 96, 121), TileType.NORMAL, 1100, (453, 377, 47, 122)),
        ("경회루", 30, (360, 295), (353, 253, 96, 120), TileType.NORMAL, 1000, (453, 253, 47, 121)),
        ("무주도", 45, (360, 150), (353, 103, 147, 147), TileType.JAIL, 0, (0, 0, 0, 0)),
        ("돈의문", 30, (520, 135), (503, 103, 120, 96), TileType.NORMAL, 1300, (503, 203, 121, 47)),
        ("해인사", 30, (645, 135), (628, 103, 120, 96), TileType.NORMAL, 1200, (627, 203, 122, 47)),
        ("종묘", 35, (780, 130), (753, 103, 120, 96), TileType.NORMAL, 1100, (752, 203, 122, 47)),
        ("숙정문", 30, (895, 135), (877, 103, 120, 96), TileType.NORMAL, 1000, (877, 203, 120, 47)),
        ("학", 45, (1050, 150), (1000, 103, 147, 147), TileType.SCHOOL, 0, (0, 0, 0, 0)),
        ("병산서원", 25, (1055, 300), (1051, 253, 96, 120), TileType.NORMAL, 1300, (1000, 253, 47, 121)),
        ("숭례문", 30, (1055, 420), (1051, 377, 96, 121), TileType.NORMAL, 1200, (1000, 377, 47, 122)),
        ("성균관", 30, (1055, 545), (1051, 502, 96, 121), TileType.NORMAL, 1100, (1000, 502, 47, 122)),
        ("북한산성", 25, (1055, 670), (1051, 627, 96, 120), TileType.NORMAL, 1000, (1000, 627, 47, 120)),
    ]
    
    tiles = []
    for idx, (name, size, name_pos, rect_info, tile_type, price, empty_rect) in enumerate(tile_info_list):
        visual = TileVisual(size, name_pos, rect_info)
        tile = Tile(name, visual, idx, tile_type, price, empty_rect)
        tiles.append(tile)
    
    return tiles
