import pygame

# 전역 상수
FONT_PATH = "board_set/font.ttf"  # 글꼴 위치
DEFAULT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = "yellow"
TEXT_COLOR = (0, 0, 0)

# 타일 시각적 표현 클래스
class TileVisual:
    def __init__(self, name_size, name_position, rect_info):
        self.name_size = name_size
        self.name_position = name_position
        self.rect = pygame.Rect(rect_info)

    def draw(self, background, name, highlight=False):
        color = HIGHLIGHT_COLOR if highlight else DEFAULT_COLOR
        pygame.draw.rect(background, color, self.rect)
        font = pygame.font.Font(FONT_PATH, self.name_size)
        rendered = font.render(name, True, TEXT_COLOR)
        background.blit(rendered, self.name_position)

# 게임 타일 클래스
class Tile:
    def __init__(self, name, visual, board_index, price=1000, empty_rect=(0,0,0,0)):
        self.name = name  # 타일 이름
        self.visual = visual  # 타일 비주얼 클래스
        self.board_index = board_index  # 인덱스 번호
        self.price = price  # 타일 가격
        self.owner = None  # 타일 주인
        self.upgrade_level = 0  # 타일 레벨
        self.toll = self.calculate_toll()  # 타일 통행료
        self.player_positions = self.generate_player_positions()  # 타일에서의 기물 위치
        self.empty_rect = empty_rect  # 타일 옆 빈 공간 rect

    def generate_player_positions(self):
        x, y, w, h = self.visual.rect
        margin = 5  # 테두리 여백
        px = x + margin
        py = y + margin
        pw = w - 2 * margin
        ph = h - 2 * margin
        # 2x2 그리드 형태
        return [
            (px + pw * 0.1, py + ph * 0.1),  # 좌상
            (px + pw * 0.6, py + ph * 0.1),  # 우상
            (px + pw * 0.1, py + ph * 0.6),  # 좌하
            (px + pw * 0.6, py + ph * 0.6),  # 우하
        ]

    def calculate_toll(self):
        if self.upgrade_level == 0:
            return int(self.price * 1.3)
        elif self.upgrade_level == 1:
            return int((self.price + 500) * 1.8)
        else:
            return int((self.price + 1500) * 2.2)

    def upgrade(self):
        if self.upgrade_level < 2:
            self.upgrade_level += 1
            self.toll = self.calculate_toll()

    def get_total_value(self):
        return self.price + (500 if self.upgrade_level == 1 else 1500 if self.upgrade_level == 2 else 0)

    def draw(self, background, mouse_pos):
        highlight = self.visual.rect.collidepoint(mouse_pos)
        self.visual.draw(background, self.name, highlight)
        # 건물(소유자) 색상 및 레벨 표시
        if self.owner is not None and hasattr(self.owner, 'color'):
            color_map = {
                'red': (255, 0, 0),
                'blue': (0, 0, 255),
                'green': (0, 128, 0),
                'yellow': (220, 220, 0)
            }
            owner_color = color_map.get(self.owner.color, (100, 100, 100))
            rect = self.visual.rect
            building_w = rect.width // 3
            building_h = rect.height // 3
            building_x = rect.x + rect.width // 2 - building_w // 2
            building_y = rect.y + rect.height // 2 - building_h // 2
            pygame.draw.rect(background, owner_color, (building_x, building_y, building_w, building_h), border_radius=6)
            # 레벨 텍스트 표시
            if self.upgrade_level > 0:
                font = pygame.font.SysFont(None, 24)
                lv_text = f"lv{self.upgrade_level}"
                text_surface = font.render(lv_text, True, (0,0,0))
                text_rect = text_surface.get_rect(center=(building_x + building_w//2, building_y + building_h//2))
                background.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.visual.rect.collidepoint(mouse_pos)

    def draw_info(self, background, pos=(50, 50)):
        # 소유자 색상 결정 (없으면 흰색)
        color_map = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 128, 0),
            'yellow': (220, 220, 0)
        }
        if self.owner is not None and hasattr(self.owner, 'color'):
            owner_color = color_map.get(self.owner.color, (255,255,255))
        else:
            owner_color = (255,255,255)
        # 박스 배경을 소유자 색상으로
        pygame.draw.rect(background, owner_color, (40, 40, 250, 200), 0)
        font = pygame.font.Font(FONT_PATH, 28)
        lines = [
            f"위치: {self.name}",
            f"가격: {self.price} 원",
            f"레벨: {self.upgrade_level}",
            f"통행료: {self.toll} 원"
        ]
        y = pos[1]
        for line in lines:
            rendered = font.render(line, True, (0,0,0))
            background.blit(rendered, (pos[0], y))
            y += 35
        pygame.draw.rect(background, (0,0,0), (40, 40, 250, 200), 3)

# 전체 타일 생성 함수
def all_tiles():
    tile_info_list = [
        # (name, name_size, name_pos, rect, price, empty_rect)
        ("출도", 45, (1030, 800), (1000, 750, 147, 147), 0, (0, 0, 0, 0)),
        ("경복궁", 30, (895, 830), (877, 801, 120, 96), 1300, (997, 801, 50, 96)),
        ("창덕궁", 30, (770, 830), (753, 801, 120, 96), 1200, (873, 801, 50, 96)),
        ("창경궁", 30, (645, 830), (628, 801, 120, 96), 1100, (748, 801, 50, 96)),
        ("덕수궁", 30, (520, 830), (503, 801, 120, 96), 1000, (623, 801, 50, 96)),
        ("미정", 45, (380, 800), (353, 750, 147, 147), 0, (0, 0, 0, 0)),
        ("남한산성", 25, (355, 670), (353, 627, 96, 120), 1300, (449, 627, 50, 120)),
        ("흥인지문", 25, (355, 545), (353, 502, 96, 121), 1200, (449, 502, 50, 121)),
        ("수원화성", 25, (355, 420), (353, 377, 96, 121), 1100, (449, 377, 50, 121)),
        ("경회루", 30, (360, 295), (353, 253, 96, 120), 1000, (449, 253, 50, 120)),
        ("무주도", 45, (360, 150), (353, 103, 147, 147), 0, (0, 0, 0, 0)),
        ("돈의문", 30, (520, 135), (503, 103, 120, 96), 1300, (623, 103, 50, 96)),
        ("해인사", 30, (645, 135), (628, 103, 120, 96), 1200, (748, 103, 50, 96)),
        ("종묘", 35, (780, 130), (753, 103, 120, 96), 1100, (873, 103, 50, 96)),
        ("숙정문", 30, (895, 135), (877, 103, 120, 96), 1000, (997, 103, 50, 96)),
        ("학", 45, (1050, 150), (1000, 103, 147, 147), 0, (0, 0, 0, 0)),
        ("병산서원", 25, (1055, 300), (1051, 253, 96, 120), 1300, (1147, 253, 50, 120)),
        ("숭례문", 30, (1055, 420), (1051, 377, 96, 121), 1200, (1147, 377, 50, 121)),
        ("성균관", 30, (1055, 545), (1051, 502, 96, 121), 1100, (1147, 502, 50, 121)),
        ("북한산성", 25, (1055, 670), (1051, 627, 96, 120), 1000, (1147, 627, 50, 120)),
    ]
    tiles = []
    for idx, (name, size, name_pos, rect_info, price, empty_rect) in enumerate(tile_info_list):
        visual = TileVisual(size, name_pos, rect_info)
        tile = Tile(name, visual, idx, price, empty_rect)
        tiles.append(tile)
    return tiles
