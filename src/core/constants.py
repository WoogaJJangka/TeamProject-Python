"""
공통 상수 (Colors, Fonts, Paths)
"""
import os

# ========== 색상 정의 (RGB) ==========
COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 128, 0),
    'yellow': (220, 220, 0),
    'light_red': (255, 180, 180),
    'light_blue': (180, 200, 255),
    'light_green': (180, 255, 180),
    'light_yellow': (255, 255, 180),
    'gray': (200, 200, 200),
    'dark_gray': (100, 100, 100),
}

# 플레이어 색상 매핑
PLAYER_COLORS = {
    'red': COLORS['red'],
    'blue': COLORS['blue'],
    'green': COLORS['green'],
    'yellow': COLORS['yellow'],
}

# 플레이어 색상 - 밝은 버전 (UI용)
PLAYER_COLORS_LIGHT = {
    'red': COLORS['light_red'],
    'blue': COLORS['light_blue'],
    'green': COLORS['light_green'],
    'yellow': COLORS['light_yellow'],
}

# ========== 리소스 경로 ==========
# 프로젝트 루트
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Assets 폴더
ASSETS_ROOT = os.path.join(PROJECT_ROOT, 'assets')
IMAGES_PATH = os.path.join(ASSETS_ROOT, 'images')
FONTS_PATH = os.path.join(ASSETS_ROOT, 'fonts')

# 기존 assets 폴더 경로 (마이그레이션 중)
LEGACY_ASSETS = {
    'game': os.path.join(PROJECT_ROOT, 'game', 'assets'),
    'roll_dices': os.path.join(PROJECT_ROOT, 'roll_dices', 'assets'),
    'board_set': os.path.join(PROJECT_ROOT, 'board_set'),
}

# ========== 폰트 설정 ==========
FONTS = {
    'default': {
        'path': os.path.join(FONTS_PATH, 'font.ttf'),
        'fallback': 'arial',  # Pygame 기본 폰트 이름
    }
}

# ========== 이미지 정의 ==========
IMAGE_PATHS = {
    'korea_map': os.path.join(IMAGES_PATH, 'korean_map.png'),
    'dice': {
        1: os.path.join(IMAGES_PATH, 'dice', 'dice1.png'),
        2: os.path.join(IMAGES_PATH, 'dice', 'dice2.png'),
        3: os.path.join(IMAGES_PATH, 'dice', 'dice3.png'),
        4: os.path.join(IMAGES_PATH, 'dice', 'dice4.png'),
        5: os.path.join(IMAGES_PATH, 'dice', 'dice5.png'),
        6: os.path.join(IMAGES_PATH, 'dice', 'dice6.png'),
    },
    'pieces': {
        'red': os.path.join(IMAGES_PATH, 'pieces', 'red.png'),
        'blue': os.path.join(IMAGES_PATH, 'pieces', 'blue.png'),
        'green': os.path.join(IMAGES_PATH, 'pieces', 'green.png'),
        'yellow': os.path.join(IMAGES_PATH, 'pieces', 'yellow.png'),
    }
}

# ========== UI 상수 ==========
CONSOLE_MAX_LINES = 8
CONSOLE_LINE_HEIGHT = 20
CONSOLE_BOX_WIDTH = 300

BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_FONT_SIZE = 18

TILE_NAME_FONT_SIZE = {
    'large': 45,
    'medium': 30,
    'small': 25,
}

INFO_BOX_WIDTH = 250
INFO_BOX_HEIGHT = 160

PLAYER_INFO_WIDTH = 250
PLAYER_INFO_HEIGHT = 150
