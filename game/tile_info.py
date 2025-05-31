import pygame

# 전역 상수: 폰트 경로 및 색상 정의
FONT_PATH = "board_set/font.ttf"  # 글꼴 위치
DEFAULT_COLOR = (255, 255, 255)    # 기본 타일 색상(흰색)
HIGHLIGHT_COLOR = "yellow"         # 하이라이트 색상(노랑)
TEXT_COLOR = (0, 0, 0)             # 텍스트 색상(검정)

# 타일의 시각적 표현을 담당하는 클래스
class TileVisual:
    def __init__(self, name_size, name_position, rect_info):
        self.name_size = name_size                # 타일 이름 폰트 크기
        self.name_position = name_position        # 타일 이름이 그려질 위치 (좌표)
        self.rect = pygame.Rect(rect_info)        # 타일의 사각형 영역(좌표, 크기)

    def draw(self, background, name, highlight=False):
        # 타일을 그리는 함수. highlight가 True면 노랑, 아니면 흰색
        color = HIGHLIGHT_COLOR if highlight else DEFAULT_COLOR
        pygame.draw.rect(background, color, self.rect)  # 타일 사각형 그리기
        font = pygame.font.Font(FONT_PATH, self.name_size)  # 폰트 설정
        rendered = font.render(name, True, TEXT_COLOR)      # 이름 텍스트 렌더링
        background.blit(rendered, self.name_position)       # 이름 출력

# 게임의 각 타일(땅, 이벤트 등)을 나타내는 클래스
class Tile:
    def __init__(self, name, visual, board_index, price=1000, empty_rect=(0,0,0,0)):
        self.name = name                  # 타일 이름
        self.visual = visual              # 타일의 시각적 표현 객체(TileVisual)
        self.board_index = board_index    # 타일의 인덱스(번호)
        self.price = price                # 타일 가격
        self.owner = None                 # 소유자(Player 객체, 없으면 None)
        self.upgrade_level = 0            # 업그레이드 레벨(0~2)
        self.toll = self.calculate_toll() # 통행료(레벨에 따라 다름)
        self.player_positions = self.generate_player_positions()  # 플레이어 말 위치
        self.empty_rect = empty_rect      # 타일 옆에 소유자 색 네모를 그릴 영역

    def generate_player_positions(self):
        # 타일 내에서 플레이어 말이 위치할 좌표(4개)를 계산
        x, y, w, h = self.visual.rect
        margin = 5
        px = x + margin
        py = y + margin
        pw = w - 2 * margin
        ph = h - 2 * margin
        # 2x2 그리드 형태로 네 위치 반환
        return [
            (px + pw * 0.1, py + ph * 0.1),  # 좌상
            (px + pw * 0.6, py + ph * 0.1),  # 우상
            (px + pw * 0.1, py + ph * 0.6),  # 좌하
            (px + pw * 0.6, py + ph * 0.6),  # 우하
        ]

    def calculate_toll(self):
        # 업그레이드 레벨에 따라 통행료 계산
        if self.upgrade_level == 0:
            return int(self.price * 1.3)
        elif self.upgrade_level == 1:
            return int((self.price + 500) * 1.8)
        else:
            return int((self.price + 1500) * 2.2)

    def upgrade(self):
        # 타일 업그레이드(최대 2)
        if self.upgrade_level < 2:
            self.upgrade_level += 1
            self.toll = self.calculate_toll()

    def get_total_value(self):
        # 타일의 총 가치(업그레이드 반영)
        return self.price + (500 if self.upgrade_level == 1 else 1500 if self.upgrade_level == 2 else 0)

    def is_clicked(self, mouse_pos):
        # 마우스 클릭이 타일 영역에 들어왔는지 확인
        return self.visual.rect.collidepoint(mouse_pos)

    def draw_info(self, background, pos=(50, 50)):
        # 타일 정보(이름, 가격, 레벨, 통행료 등)를 화면에 출력
        # empty_rect와 동일한 연한 파스텔톤 색상 사용
        color_map = {
            'red': (255, 180, 180),      # 연한 빨강
            'blue': (180, 200, 255),     # 연한 파랑
            'green': (180, 255, 180),    # 연한 초록
            'yellow': (255, 255, 180)    # 연한 노랑
        }
        # 소유자 색상(없으면 흰색)
        if self.owner is not None and hasattr(self.owner, 'color'):
            owner_color = color_map.get(self.owner.color, (255,255,255))
        else:
            owner_color = (255,255,255)
        # 정보 박스 배경을 소유자 색상으로 그림
        pygame.draw.rect(background, owner_color, (40, 40, 250, 160), 0)
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
        # 정보 박스 테두리
        pygame.draw.rect(background, (0,0,0), (40, 40, 250, 160), 3)

    def draw_owner_box(self, background):
        # empty_rect(타일 옆 네모)에 소유자 색을 칠함
        # 0, 5, 10, 15번 타일은 제외(이벤트 칸)
        if hasattr(self, 'board_index') and self.board_index not in [0, 5, 10, 15]:
            x, y, w, h = self.empty_rect
            if w > 0 and h > 0:
                # 기존 색상보다 더 밝은 파스텔톤으로 지정
                color_map = {
                    'red': (255, 180, 180),      # 연한 빨강
                    'blue': (180, 200, 255),     # 연한 파랑
                    'green': (180, 255, 180),    # 연한 초록
                    'yellow': (255, 255, 180)    # 연한 노랑
                }
                owner_color = (255, 255, 255)  # 기본: 흰색
                if self.owner is not None and hasattr(self.owner, 'color'):
                    c = self.owner.color
                    if isinstance(c, tuple) and len(c) == 3:
                        # RGB 튜플이면 밝게 변환
                        owner_color = tuple(min(255, int(v + (255-v)*0.6)) for v in c)
                    elif c in color_map:
                        owner_color = color_map[c]
                    else:
                        owner_color = (255, 200, 200)  # 알 수 없는 색은 연한 빨강
                pygame.draw.rect(background, owner_color, (x, y, w, h))

# 전체 타일 생성 함수: 보드에 배치될 모든 타일을 생성해 리스트로 반환
# 각 타일의 이름, 폰트 크기, 이름 위치, 사각형 영역, 가격, empty_rect(소유자 네모) 좌표를 지정
# empty_rect는 타일 옆에 위치한 작은 네모로, 소유자 색을 표시하는 용도

def all_tiles():
    tile_info_list = [
        # (name, name_size, name_pos, rect, price, empty_rect)
        ("출도", 45, (1030, 800), (1000, 750, 147, 147), 0, (0, 0, 0, 0)),
        ("경복궁", 30, (895, 830), (877, 801, 120, 96), 1300, (877, 750, 120, 47)),
        ("창덕궁", 30, (770, 830), (753, 801, 120, 96), 1200, (752, 750, 122, 47)),
        ("창경궁", 30, (645, 830), (628, 801, 120, 96), 1100, (627, 750, 122, 47)),
        ("덕수궁", 30, (520, 830), (503, 801, 120, 96), 1000, (503, 750, 121, 47)),
        ("미정", 45, (380, 800), (353, 750, 147, 147), 0, (0, 0, 0, 0)),
        ("남한산성", 25, (355, 670), (353, 627, 96, 120), 1300, (453, 627, 47, 120)),
        ("흥인지문", 25, (355, 545), (353, 502, 96, 121), 1200, (453, 502, 47, 122)),
        ("수원화성", 25, (355, 420), (353, 377, 96, 121), 1100, (453, 377, 47, 122)),
        ("경회루", 30, (360, 295), (353, 253, 96, 120), 1000, (453, 253, 47, 121)),
        ("무주도", 45, (360, 150), (353, 103, 147, 147), 0, (0, 0, 0, 0)),
        ("돈의문", 30, (520, 135), (503, 103, 120, 96), 1300, (503, 203, 121, 47)),
        ("해인사", 30, (645, 135), (628, 103, 120, 96), 1200, (627, 203, 122, 47)),
        ("종묘", 35, (780, 130), (753, 103, 120, 96), 1100, (752, 203, 122, 47)),
        ("숙정문", 30, (895, 135), (877, 103, 120, 96), 1000, (877, 203, 120, 47)),
        ("학", 45, (1050, 150), (1000, 103, 147, 147), 0, (0, 0, 0, 0)),
        ("병산서원", 25, (1055, 300), (1051, 253, 96, 120), 1300, (1000, 253, 47, 121)),
        ("숭례문", 30, (1055, 420), (1051, 377, 96, 121), 1200, (1000, 377, 47, 122)),
        ("성균관", 30, (1055, 545), (1051, 502, 96, 121), 1100, (1000, 502, 47, 122)),
        ("북한산성", 25, (1055, 670), (1051, 627, 96, 120), 1000, (1000, 627, 47, 120)),
    ]
    tiles = []
    for idx, (name, size, name_pos, rect_info, price, empty_rect) in enumerate(tile_info_list):
        visual = TileVisual(size, name_pos, rect_info)  # 타일 시각 객체 생성
        tile = Tile(name, visual, idx, price, empty_rect)  # 타일 객체 생성
        tiles.append(tile)

    return tiles