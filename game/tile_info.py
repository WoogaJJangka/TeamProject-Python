import pygame

# 전역 상수
FONT_PATH = "board_set/font.ttf" # 글꼴 위치
DEFAULT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = "yellow"
TEXT_COLOR = (0, 0, 0)

# 시각적 클래스
class TileVisual: # 특정 타일 노란색 하이라이트로 변경
    def __init__(self, name_size, name_position, rect_info):
        self.name_size = name_size
        self.name_position = name_position
        self.rect = pygame.Rect(rect_info)

    def draw(self, backgruond, name, highlight=False):
        color = HIGHLIGHT_COLOR if highlight else DEFAULT_COLOR
        pygame.draw.rect(backgruond, color, self.rect)

        font = pygame.font.Font(FONT_PATH, self.name_size)
        rendered = font.render(name, True, TEXT_COLOR)
        backgruond.blit(rendered, self.name_position)


# 게임 타일 클래스
class Tile:
    def __init__(self, name, visual, board_index, price=1000):
        self.name = name # 타일 이름
        self.visual = visual # 타일 비주얼 클래스
        self.board_index = board_index # 인덱스 번호
        self.price = price # 타일 가격
        self.owner = None # 타일 주인
        self.upgrade_level = 0 # 타일 레벨
        self.toll = self.calculate_toll() # 타일 통행료
        self.player_positions = self.generate_player_positions() # 타일에서의 기물 위치

    def generate_player_positions(self): # 기물 위치 정해주는 메서드

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

    def calculate_toll(self): # 타일 통행료 메서드
        if self.upgrade_level == 0:
            return int(self.price * 1.3)
        elif self.upgrade_level == 1:
            return int((self.price + 500) * 1.8)
        else:
            return int((self.price + 1500) * 2.2)

    def upgrade(self): # 타일 업그레이드 메서드
        if self.upgrade_level < 2:
            self.upgrade_level += 1
            self.toll = self.calculate_toll() # 바로 위에 함수 부르기

    def get_total_value(self): # 타일 업그레이드 금액
        return self.price + (500 if self.upgrade_level == 1 else 1500 if self.upgrade_level == 2 else 0)

    def draw(self, background, mouse_pos): # 타일 하이라이트
        highlight = self.visual.rect.collidepoint(mouse_pos)
        self.visual.draw(background, self.name, highlight) # TileVisual의 draw 불러오기

    def is_clicked(self, mouse_pos): # 마우스 클릭
        return self.visual.rect.collidepoint(mouse_pos)

    def draw_info(self, background, pos=(50, 50)): # 왼쪽 상단에 타일에 대한 정보 표시
        pygame.draw.rect(background, (255,255,255), (40, 40, 250, 200), 500)

        font = pygame.font.Font(FONT_PATH, 28)
        lines = [
            f"위치: {self.name}",
            f"가격: {self.price} 원",
            f"레벨: {self.upgrade_level}",
            f"통행료: {self.toll} 원",
            f"소유자: {self.owner if self.owner else '없음'}"
        ]
        y = pos[1]
        for line in lines:
            rendered = font.render(line, True, (0,0,0))
            background.blit(rendered, (pos[0], y))
            y += 35  # 줄 간격


def all_tiles(): # 모든 타일 정보 정리하기해서 리스트로 반환
    tile_info_list = [
        # (name, name_size, name_pos, rect, board_index, price)
        ("출도", 45, (1030, 800), (1000, 750, 147, 147), 0, 0),
        ("북한산성", 25, (1055, 670), (1051, 627, 96, 120), 1, 1000),
        ("성균관", 30, (1055, 545), (1051, 502, 96, 121), 2, 1100),
        ("숭례문", 30, (1055, 420), (1051, 377, 96, 121), 3, 1200),
        ("병산서원", 25, (1055, 300), (1051, 253, 96, 120), 4, 1300),
        ("학", 45, (1050, 150), (1000, 103, 147, 147), 5, 0),
        ("숙정문", 30, (895, 135), (877, 103, 120, 96), 6, 1000),
        ("종묘", 35, (780, 130), (753, 103, 120, 96), 7, 1100),
        ("해인사", 30, (645, 135), (628, 103, 120, 96), 8, 1200),
        ("돈의문", 30, (520, 135), (503, 103, 120, 96), 9, 1300),
        ("무주도", 45, (360, 150), (353, 103, 147, 147), 10, 0),
        ("경회루", 30, (360, 295), (353, 253, 96, 120), 11, 1000),
        ("수원화성", 25, (355, 420), (353, 377, 96, 121), 12, 1100),
        ("흥인지문", 25, (355, 545), (353, 502, 96, 121), 13, 1200),
        ("남한산성", 25, (355, 670), (353, 627, 96, 120), 14, 1300),
        ("미정", 45, (380, 800), (353, 750, 147, 147), 15, 0),
        ("덕수궁", 30, (520, 830), (503, 801, 120, 96), 16, 1000),
        ("창경궁", 30, (645, 830), (628, 801, 120, 96), 17, 1100),
        ("창덕궁", 30, (770, 830), (753, 801, 120, 96), 18, 1200),
        ("경복궁", 30, (895, 830), (877, 801, 120, 96), 19, 1300),
    ]

    tiles = []
    for name, size, name_pos, rect_info, index, price in tile_info_list:
        visual = TileVisual(size, name_pos, rect_info)
        tile = Tile(name, visual, index, price)
        tiles.append(tile)

    return tiles