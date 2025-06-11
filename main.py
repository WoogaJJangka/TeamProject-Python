# --- 라이브러리 및 모듈 임포트 ---
import pygame  # pygame: 파이썬 게임 개발용 라이브러리
import os  # os: 파일 경로 조작 등 운영체제 기능 사용
from board_set.BoardScreen import BoardScreen  # 보드 화면 그리기 클래스 (보드판 이미지 및 타일 배치)
from roll_dices.roller import DiceRoller      # 주사위 굴리기 클래스 (주사위 이미지, 애니메이션 등)
from game.tile_info import all_tiles           # 타일 정보 및 타일 객체 생성 함수
import game.game_manager as gm                 # 게임 상태 관리 클래스 (턴, 타일, 플레이어 등)
import game.player as player                   # 플레이어 클래스 (플레이어 속성, 이동 등)

print("게임 시작")  # 디버깅용 시작 메시지 (실행 확인)

# --- pygame 초기화 및 화면 설정 ---
pygame.init()  # pygame 라이브러리 내부 상태 초기화 (필수)
clock = pygame.time.Clock()  # 프레임 조절용 시계 객체 (게임 루프 속도 제어)
background = pygame.display.set_mode((1500, 1000))  # 게임 창 크기(픽셀) 설정
background.fill((255, 255, 255))  # 배경을 흰색으로 채움 (RGB)

# --- 보드 배경 및 타일 배치 ---
BoardScreen(background)  # 보드판 이미지와 타일 시각 객체를 화면에 배치

# --- 게임 주요 객체 생성 ---
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))  # 주사위 객체 (이미지, 애니메이션)
game_manager = gm.GameManager()  # 게임 상태 관리 객체 (플레이어, 타일, 턴 등)
tiles = game_manager.tiles  # 전체 타일 리스트 (game_manager에서 반드시 가져와야 일관성 유지)

# --- 플레이어 말 이미지 로딩 및 연결 ---
PLAYER_IMAGE_PATHS = {
    'red': os.path.join("game", "assets", "red.png"),    # 빨간색 플레이어 말 이미지 경로
    'blue': os.path.join("game", "assets", "blue.png"),   # 파란색 플레이어 말 이미지 경로
    'green': os.path.join("game", "assets", "green.png"), # 초록색 플레이어 말 이미지 경로
    'yellow': os.path.join("game", "assets", "yellow.png"),# 노란색 플레이어 말 이미지 경로
}
PLAYER_IMAGES = {}  # 색상별 이미지 객체 저장 딕셔너리
for color, path in PLAYER_IMAGE_PATHS.items():
    img = pygame.image.load(path)  # 이미지 파일 로드
    img = pygame.transform.scale(img, (40, 40))  # 말 크기 40x40으로 조정
    PLAYER_IMAGES[color] = img
# 각 Player 객체에 이미지 연결 (piece_image 속성 추가)
for p in game_manager.players:
    p.piece_image = PLAYER_IMAGES[p.color]

# --- 이동 후 도착 타일 이벤트 통합 함수 ---
def handle_tile_event_after_move(current_player, player_index):
    """
    플레이어가 이동(일반, 더블, 순간이동 등) 후 도착한 타일에서 발생하는 모든 이벤트를 일관되게 처리하는 함수입니다.
    - 특수 타일(출도, 학, 무주도, 미정) 도착 시 각 타일별 고유 이벤트를 실행합니다.
    - 일반 땅 도착 시 구매/업그레이드/통행료/이벤트를 처리합니다.
    - 이 함수는 이동 후 도착 타일 이벤트의 중복 분기와 코드 중복을 제거하고, 모든 이동 방식(무주도 탈출, 텔레포트 포함)에서 일관된 이벤트 처리를 보장합니다.
    """
    global ask_buy, buy_tile_index, buy_player_index, buy_buttons
    global ask_upgrade, upgrade_tile_index, upgrade_player_index, upgrade_buttons
    arrived_tile = tiles[current_player.position]  # 도착한 타일 객체
    special_tile_names = ["출도", "학", "무주도", "미정"]  # 특수 타일 이름 목록
    add_console_message(f"{current_player.color} 플레이어가 {arrived_tile.name} 칸에 도착했습니다.")
    # --- 특수 타일별 분기 ---
    if current_player.position == 0:  # 출도 칸
        current_player.money += 2000  # 출도 보너스 지급
        add_console_message(f"{current_player.color} 플레이어가 출도 칸에 도착했습니다. 2000원을 받았습니다.")
        game_manager.turn_over()  # 턴 넘김
    elif current_player.position == 5:  # 미정 칸
        # 소유한 땅이 있으면 업그레이드 시도, 없으면 메시지 출력
        if current_player.properties:
            upgraded = False
            for upgrade_tile in current_player.properties:
                upgrade_tile_index = tiles.index(upgrade_tile)
                success, message = game_manager.upgrade_tile(upgrade_tile_index, player_index)
                if success:
                    add_console_message(f"미정 칸 효과: {upgrade_tile.name} 땅이 업그레이드 되었습니다!")
                    upgraded = True
                    break
                else:
                    add_console_message(f"미정 칸 효과: {upgrade_tile.name} 업그레이드 실패 - {message}")
            if not upgraded:
                add_console_message("미정 칸 효과: 업그레이드 가능한 땅이 없습니다.")
        else:
            add_console_message("미정 칸 효과: 소유한 땅이 없어 업그레이드할 수 없습니다.")
        game_manager.turn_over()  # 턴 넘김
        return True
    elif current_player.position == 10:  # 무주도 칸
        current_player.stop_turns = 2  # 2턴 이동 불가
        add_console_message(f"{current_player.color} 플레이어는 무주도에 도착해 2턴간 이동할 수 없습니다.")
        game_manager.turn_over()  # 턴 넘김
        return True
    elif current_player.position == 15:  # 학 칸
        add_console_message("학 칸에 도착했습니다! 원하는 타일을 클릭해 이동하세요.")
        draw_console_messages(background)
        pygame.display.update()
        teleport_done = False
        while not teleport_done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for idx, tile in enumerate(tiles):
                        if tile.is_clicked(mouse_pos):
                            if idx == 15:
                                add_console_message("학 타일로는 순간이동할 수 없습니다.")
                            else:
                                success, message = game_manager.teleport_player(player_index, idx)
                                add_console_message(message)
                                teleport_done = True
                                break
                elif event.type == pygame.QUIT:
                    return False  # 게임 종료
            # 순간이동 선택 중에도 타일 하이라이트 적용 (UI 피드백)
            mouse_pos = pygame.mouse.get_pos()
            highlight_tile = None
            for tile in tiles:
                if tile.visual.rect.collidepoint(mouse_pos):
                    highlight_tile = tile
                    break
            for tile in tiles:
                if tile is highlight_tile:
                    tile.visual.draw(background, tile.name, highlight=True)
                else:
                    tile.visual.draw(background, tile.name, highlight=False)
            if highlight_tile:
                highlight_tile.draw_info(background, pos=(50, 50))
            for idx, p in enumerate(game_manager.players):
                p.draw_info(background, pos=(1200, 50 + idx * 160))
            pygame.display.update()
        # 순간이동 후 재귀적으로 이벤트 처리 (이동한 타일에서 다시 이벤트 발생)
        return handle_tile_event_after_move(current_player, player_index)
    else:
        # --- 일반 타일(구매/업그레이드/통행료/이벤트) ---
        if arrived_tile.owner is None and hasattr(arrived_tile, "price") and arrived_tile.price > 0 and arrived_tile.name not in special_tile_names:
            # 소지금 부족 시 바로 메시지 출력 후 턴 넘김
            if current_player.money < arrived_tile.price:
                add_console_message(f"{current_player.color} 플레이어는 {arrived_tile.name}을(를) 구매할 돈이 부족합니다.")
                game_manager.turn_over()
            # 구매 질문 상태 진입 (버튼 표시)
            ask_buy = True
            buy_tile_index = current_player.position
            buy_player_index = player_index
            font_btn = pygame.font.Font("board_set/font.ttf", 18)
            buy_buttons = [
                Button((60, background.get_height()-140, 80, 40), "예", font_btn),
                Button((160, background.get_height()-140, 80, 40), "아니요", font_btn)
            ]
            return True
        elif arrived_tile.owner == current_player and hasattr(arrived_tile, "price") and arrived_tile.price > 0 and arrived_tile.upgrade_level < 2:
            # 업그레이드 비용 부족 시 바로 메시지 출력 후 턴 넘김
            upgrade_cost = 500 if arrived_tile.upgrade_level == 0 else 1000
            if current_player.money < upgrade_cost:
                add_console_message(f"{current_player.color} 플레이어는 업그레이드 비용 ₩{upgrade_cost}가 부족합니다.")
                game_manager.turn_over()
            # 업그레이드 질문 상태 진입 (버튼 표시)
            ask_upgrade = True
            upgrade_tile_index = current_player.position
            upgrade_player_index = player_index
            font_btn = pygame.font.Font("board_set/font.ttf", 18)
            upgrade_buttons = [
                Button((60, background.get_height()-140, 80, 40), "예", font_btn),
                Button((160, background.get_height()-140, 80, 40), "아니요", font_btn)
            ]
            return True
        else:
            # 타인 소유 땅 등 기타 이벤트 처리
            success, message = game_manager.tile_event(current_player.position, player_index)
            if message:
                add_console_message(message)
            game_manager.turn_over()
            winner_tuple = game_manager.check_winner()
            winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
            if winner:
                add_winner_message(winner, reason)
                return False
            return True

# --- 콘솔 메시지 리스트와 최대 줄 수 설정 ---
console_messages = []  # 최근 메시지 4개 저장 (최신순)
MAX_CONSOLE_LINES = 8  # 콘솔에 표시할 최대 줄 수

# --- 콘솔 메시지 추가 함수 ---
def add_console_message(msg):
    """
    콘솔 메시지 리스트에 메시지를 추가하고, 최대 줄 수를 초과하면 마지막 메시지를 삭제합니다.
    - msg가 리스트면 각 메시지를 개별적으로 추가
    - 항상 최신 메시지가 위에 오도록 insert(0, ...)
    - print로도 출력 (터미널 디버깅)
    """
    if isinstance(msg, list):
        for m in msg:
            console_messages.insert(0, str(m))
            print(str(m))
    else:
        console_messages.insert(0, str(msg))
        print(str(msg))
    while len(console_messages) > MAX_CONSOLE_LINES:
        console_messages.pop()

# --- 콘솔 메시지 그리기 함수 ---
def draw_console_messages(surface):
    """
    콘솔 메시지 리스트를 화면 왼쪽 중앙에 출력합니다.
    - 폰트 크기 16, 최대 8줄, 흰색 배경 박스 위에 표시
    - 한 줄이 너무 길면 자동 줄바꿈
    - 최신 메시지가 아래쪽에 오도록 역순 출력
    """
    font = pygame.font.Font("board_set/font.ttf", 16)
    start_y = background.get_height() // 2 - (MAX_CONSOLE_LINES * 20)
    box_width = 300
    box_height = MAX_CONSOLE_LINES * 80  # 충분히 크게
    s = pygame.Surface((box_width, box_height))
    s.fill((255, 255, 255))
    surface.blit(s, (40, start_y - 2))
    max_chars = 22  # 한 줄 최대 글자수
    y = start_y + (MAX_CONSOLE_LINES - 1) * 20  # 가장 아래에서 시작
    all_lines = []
    for msg in console_messages:
        lines = [msg[i:i+max_chars] for i in range(0, len(msg), max_chars)]
        all_lines.extend(lines[::-1])  # 줄바꿈된 라인을 역순으로 추가 (아래줄이 먼저 나오게)
    all_lines = all_lines[:MAX_CONSOLE_LINES]  # 최대 줄 수만큼만 출력
    for line in all_lines:
        rendered = font.render(line, True, (30, 30, 30))
        surface.blit(rendered, (45, y))
        y -= 20
        if y < start_y - 20:
            break

# --- Button 클래스 (UI 버튼) ---
class Button:
    """
    게임 내에서 예/아니요 등 선택지 버튼을 그릴 때 사용하는 UI 클래스
    - rect: 버튼 위치와 크기 (pygame.Rect)
    - text: 버튼에 표시할 텍스트
    - font: 폰트 객체
    - color: 버튼 배경색
    - text_color: 텍스트 색상
    """
    def __init__(self, rect, text, font, color=(200,200,200), text_color=(0,0,0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        # 버튼 사각형과 테두리, 텍스트를 화면에 그림
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (100,100,100), self.rect, 2)
        rendered = self.font.render(self.text, True, self.text_color)
        text_rect = rendered.get_rect(center=self.rect.center)
        surface.blit(rendered, text_rect)

    def is_clicked(self, pos):
        # 마우스 좌표 pos가 버튼 영역에 포함되는지 판정
        return self.rect.collidepoint(pos)

# --- 구매/업그레이드 관련 상태 변수 (전역) ---
ask_buy = False  # 구매 여부 질문 상태 (True면 버튼 표시)
buy_tile_index = None  # 구매 대상 타일 인덱스
buy_player_index = None  # 구매 시도 플레이어 인덱스
buy_buttons = []  # 구매 버튼 리스트
ask_upgrade = False  # 업그레이드 여부 질문 상태
upgrade_tile_index = None  # 업그레이드 대상 타일 인덱스
upgrade_player_index = None  # 업그레이드 시도 플레이어 인덱스
upgrade_buttons = []  # 업그레이드 버튼 리스트

# --- 파산 플레이어 턴 넘김 및 우승자 체크 함수 ---
def skip_bankrupt_and_check_winner():
    """
    [공통 처리 함수] 파산한 플레이어의 차례는 자동으로 넘기고,
    우승자가 발생하면 우승 메시지를 출력하고 게임을 종료(running=False)합니다.
    - while 루프를 통해 연속적으로 파산 플레이어를 건너뜀
    - 우승자 발생 시 add_winner_message()로 메시지 출력 후 False 반환(게임 루프 종료)
    - 우승자 없으면 True 반환(게임 계속)
    """
    global running
    while game_manager.get_current_player().is_bankrupt:
        add_console_message(f"{game_manager.get_current_player_color()} 플레이어는 파산했으므로 턴을 옮깁니다.")
        game_manager.turn_over()
        winner_tuple = game_manager.check_winner()
        winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
        if winner:
            add_winner_message(winner, reason)  # 우승자 메시지 일관 출력 함수
            running = False
            return False
    return True

# --- 우승 메시지 출력 함수 (중복 제거) ---
def add_winner_message(winner, reason):
    """
    [공통 처리 함수] 우승자와 우승 사유에 따라 일관된 메시지를 출력합니다.
    - bankruptcy: 파산으로 인한 우승
    - property: 땅 개수로 인한 우승
    - 기타: 일반 우승
    """
    if reason == 'bankruptcy':
        add_console_message(f"{winner.color} 플레이어를 제외한 모두가 파산했습니다. {winner.color} 플레이어 우승!")
    elif reason == 'property':
        add_console_message(f"땅 개수 차이로 {winner.color} 플레이어 우승!")
    else:
        add_console_message(f"{getattr(winner, 'color', str(winner))} 플레이어가 우승했습니다!")

# --- 메인 게임 루프 ---
running = True  # 게임 실행 상태 (False가 되면 루프 종료)

while running:  # 게임이 실행중인 동안 반복
    clock.tick(120)  # 프레임 제한 (초당 최대 120회 루프)

    # --- 파산한 플레이어의 차례는 자동으로 넘김 ---
    # (우승자 발생 시 add_winner_message로 메시지 출력 후 running=False)
    if not skip_bankrupt_and_check_winner():  # 파산 플레이어 자동 스킵 및 우승자 발생 시 게임 종료
        break

    mouse_pos = pygame.mouse.get_pos()  # 마우스 위치 (타일 하이라이트, 클릭 등 UI용)

    # --- 타일 하이라이트 및 정보 표시 ---
    highlight_tile = None
    for tile in tiles:
        if tile.visual.rect.collidepoint(mouse_pos):
            highlight_tile = tile
            break
    for tile in tiles:
        highlight = tile.visual.rect.collidepoint(mouse_pos)
        tile.draw_owner_box(background)  # 타일 소유자 박스(색상) 그리기
        tile.visual.draw(background, tile.name, highlight)  # 타일 이미지 및 이름 그리기

    # --- 타일 정보창 표시 (마우스 올린 타일 or 현재 플레이어 위치) ---
    if highlight_tile:
        highlight_tile.draw_info(background, pos=(50, 50))  # 마우스가 올려진 타일의 상세 정보 표시 (좌측 상단)
    else:
        current_tile = tiles[game_manager.get_current_player().position]
        current_tile.draw_info(background, pos=(50, 50))  # 마우스를 올리지 않은 경우, 현재 플레이어가 위치한 타일 정보 표시

    # --- 플레이어 정보창 및 말 그리기 ---
    for idx, p in enumerate(game_manager.players):
        p.draw_info(background, pos=(1200, 50 + idx * 160))  # 각 플레이어의 정보(이름, 돈, 소유 땅 등)를 우측에 표시
    for idx in range(len(game_manager.players)):
        pygame.draw.rect(background, (255,255,255), (1195, 45 + idx*160, 260, 160), 4)  # 각 플레이어 정보창에 흰색 테두리
    idx = game_manager.current_player_index
    pygame.draw.rect(background, (255,0,0), (1195, 45 + idx*160, 260, 160), 4)  # 현재 턴인 플레이어의 정보창만 빨간색 테두리로 강조
    for idx, p in enumerate(game_manager.players):
        tile = tiles[p.position]  # 플레이어가 위치한 타일 객체
        orig_pos = tile.player_positions[p.turn]  # 해당 타일에서 플레이어 말의 기본 위치(좌표)
        pos = (orig_pos[0] + 10, orig_pos[1] + 10)  # 말 위치를 약간 보정하여 겹침 방지
        img_rect = p.piece_image.get_rect(center=(int(pos[0]), int(pos[1])))  # 말 이미지의 중심 좌표 계산
        background.blit(p.piece_image, img_rect)  # 실제로 말 이미지를 보드에 그림

    # --- 콘솔 메시지 그리기 ---
    draw_console_messages(background)  # 좌측 중앙에 최근 게임 메시지(이벤트, 안내 등) 출력

    # --- 구매/업그레이드 질문 및 버튼 그리기 ---
    if ask_buy:
        font_q = pygame.font.Font("board_set/font.ttf", 18)
        question = font_q.render("땅을 구매하겠습니까?", True, (0,0,0))
        background.blit(question, (60, background.get_height()-180))  # 질문 텍스트를 좌측 하단에 표시
        for btn in buy_buttons:
            btn.draw(background)  # 예/아니요 버튼을 그리기
    if ask_upgrade:
        font_q = pygame.font.Font("board_set/font.ttf", 18)
        question = font_q.render("땅을 업그레이드 하시겠습니까?", True, (0,0,0))
        background.blit(question, (60, background.get_height()-180))  # 업그레이드 질문 텍스트
        for btn in upgrade_buttons:
            btn.draw(background)  # 업그레이드 예/아니요 버튼

    # --- pygame 이벤트 처리 (마우스, 키보드 등) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # [이벤트] 창 닫기 버튼 클릭 시 게임 종료

        # 타일 구매 이벤트 처리 (구매 질문 상태에서만 동작)
        elif ask_buy and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 구매 버튼(예/아니요) 클릭 판정
            for idx, btn in enumerate(buy_buttons):
                if btn.is_clicked(event.pos):  # 해당 버튼이 클릭되었는지 확인
                    if idx == 0:  # 예 버튼 클릭 시
                            success, message = game_manager.buy_tile(buy_tile_index, buy_player_index)  # 타일 구매 시도
                            add_console_message(message)  # 구매 결과 메시지 출력
                    else:  # 아니요 버튼 클릭 시
                        add_console_message("구매를 취소했습니다.")
                    # 구매 상태 변수 초기화 (질문 종료)
                    ask_buy = False
                    buy_tile_index = None
                    buy_player_index = None
                    buy_buttons = []
                    game_manager.turn_over()  # 턴 넘김 (구매 여부와 무관하게)
                    # 구매 후 파산 등으로 인한 우승자 체크
                    winner_tuple = game_manager.check_winner()
                    winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
                    if winner:
                        add_winner_message(winner, reason)  # 우승 메시지 출력
                        running = False
                    break

        # 타일 업그레이드 이벤트 처리 (업그레이드 질문 상태에서만 동작)
        elif ask_upgrade and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 업그레이드 버튼(예/아니요) 클릭 판정
            for idx, btn in enumerate(upgrade_buttons):
                if btn.is_clicked(event.pos):  # 해당 버튼이 클릭되었는지 확인
                    if idx == 0:  # 예 버튼 클릭 시
                        success, message = game_manager.upgrade_tile(upgrade_tile_index, upgrade_player_index)  # 업그레이드 시도
                        add_console_message(message)  # 업그레이드 결과 메시지 출력
                    else:
                        add_console_message("업그레이드를 취소했습니다.")
                    # 업그레이드 상태 변수 초기화 (질문 종료)
                    ask_upgrade = False
                    upgrade_tile_index = None
                    upgrade_player_index = None
                    upgrade_buttons = []
                    game_manager.turn_over()  # 턴 넘김 (업그레이드 여부와 무관하게)

        # 일반적인 키보드 이벤트 처리 (주사위 굴리기, 디버깅 핫키 등)
        elif not ask_buy and not ask_upgrade and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # [스페이스바] 현재 플레이어의 차례에 주사위 굴리기
                current_player = game_manager.get_current_player()  # 현재 차례 플레이어 객체
                add_console_message(f"{current_player.color} 플레이어의 턴입니다.")
                dice_pos = (44, 600)  # 항상 왼쪽 지정 위치에 주사위 표시
                if current_player.is_bankrupt:
                    # 파산 상태면 턴 넘김 (아무 동작 없음)
                    add_console_message(f"{game_manager.get_current_player_color()} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
                    game_manager.turn_over()
                elif getattr(current_player, 'stop_turns', 0) > 0:
                    # 무주도 등 이동불가 상태면 주사위 굴리기
                    add_console_message(f"{current_player.color} 플레이어는 이동불가 상태입니다. (남은 턴: {current_player.stop_turns})")
                    dice1, dice2, message = roller.roll_two_dice(group_pos=dice_pos)  # 주사위 굴리기
                    add_console_message(message)
                    if dice1 == dice2:
                        # 더블이 나오면 즉시 이동 및 이동불가 해제
                        steps = dice1 + dice2
                        current_player.move(steps)  # 플레이어 이동
                        add_console_message(f"두 눈이 같아 {steps}칸 이동합니다!")
                        current_player.stop_turns = 0  # 이동불가 해제
                        # 더블 보너스 지급 없음 (무주도에서 나올 때)
                        player_index = game_manager.current_player_index
                        result = handle_tile_event_after_move(current_player, player_index)  # 도착 타일 이벤트 처리
                        if result is False:
                            running = False
                            break
                    else:
                        # 더블이 아니면 이동불가 턴 차감 후 턴 넘김
                        add_console_message("이동하지 못합니다.")
                        current_player.stop_turns -= 1
                        game_manager.turn_over()
                else:
                    # 일반 이동: 더블이면 즉시 재굴림, 누적 이동, 더블이 아닐 때만 이동 후 이벤트
                    steps = 0  # 누적 이동 칸수
                    double_count = 0  # 더블 횟수 카운트 (더블이 몇 번 나왔는지 추적)
                    while True:
                        dice1, dice2 , message = roller.roll_two_dice(group_pos=dice_pos)  # 주사위 두 개를 굴림
                        add_console_message(message)  # 주사위 결과 메시지 출력
                        steps += dice1 + dice2  # 이번에 나온 주사위 눈의 합을 누적 이동 칸수에 더함
                        if dice1 == dice2:
                            # 더블(두 눈이 같음)이 나오면
                            double_count += 1  # 더블 횟수 증가
                            current_player.money += 500  # 플레이어에게 500원 보너스 지급
                            add_console_message(f"더블 보너스! 500원을 받았습니다.")  # 콘솔에 안내 메시지 출력
                            continue  # 턴을 넘기지 않고 즉시 다시 주사위 굴림(steps 누적)
                        else:
                            # 더블이 아니면 반복 종료, 누적 steps만큼 이동
                            break
                    current_player.move(steps)  # 누적된 칸수만큼 플레이어 이동
                    add_console_message(f"{current_player.color} 플레이어가  {steps}칸 이동했습니다.")
                    player_index = game_manager.current_player_index
                    result = handle_tile_event_after_move(current_player, player_index)  # 도착 타일 이벤트 처리
                    if result is False:
                        running = False
                        break
            elif event.key == pygame.K_p and pygame.key.get_pressed()[pygame.K_F1]:
                # [F1+P] 모든 플레이어 위치 출력 (디버깅용 핫키)
                add_console_message(f'현제 플레이어들의 위치: {[p.position for p in game_manager.players]}')
            elif event.key == pygame.K_m and pygame.key.get_pressed()[pygame.K_F1]:
                # [F1+M] 모든 플레이어 돈 출력 (디버깅용 핫키)
                add_console_message(f'현제 플레이어들의 돈: {[p.money for p in game_manager.players]}')
            elif event.key == pygame.K_t and pygame.key.get_pressed()[pygame.K_F1]:
                # [F1+T] 플레이어 순간이동 (디버깅용 핫키, 콘솔 입력 필요)
                selected_player_index = int(input("플레이어 인덱스를 입력하세요 (0-3): "))
                destination_tile_index = int(input("이동할 타일의 인덱스를 입력하세요 (0-19): "))
                game_manager.teleport_player(selected_player_index, destination_tile_index)  # 순간이동 함수 호출
        elif not ask_buy and not ask_upgrade and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # [일반 상태] 타일 클릭 시 타일명 콘솔 출력 (정보 확인용, UI 상호작용)
            for idx, tile in enumerate(tiles):
                if tile.is_clicked(mouse_pos):
                    add_console_message(f"{tile.name} 타일 클릭")  # 콘솔 메시지 추가 함수
                    break
    pygame.display.update()  # 화면 업데이트 함수 (모든 그리기 후 반드시 호출)

print("프로그램 종료") # 디버깅용 종료 메시지 (실행 확인)
pygame.quit()  # 게임 종료 함수 (메인 루프 탈출 시)