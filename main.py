import pygame
import os
from board_set.BoardScreen import BoardScreen
from roll_dices.roller import DiceRoller
from game.tile_info import all_tiles
import game.game_manager as gm
import game.player as player

print("게임 시작1")
# pygame 초기화 및 화면 설정
pygame.init()
clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))

# 보드 배경 그리기
BoardScreen(background)


# 타일 및 객체 생성
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))
game_manager = gm.GameManager()
tiles = game_manager.tiles  # 반드시 game_manager.tiles만 사용

# --- 플레이어 말 이미지 로딩 및 연결 ---
PLAYER_IMAGE_PATHS = {
    'red': os.path.join("game", "assets", "red.png"),
    'blue': os.path.join("game", "assets", "blue.png"),
    'green': os.path.join("game", "assets", "green.png"),
    'yellow': os.path.join("game", "assets", "yellow.png"),
}
PLAYER_IMAGES = {}
for color, path in PLAYER_IMAGE_PATHS.items():
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (40, 40))  # 말 크기 조정
    PLAYER_IMAGES[color] = img
# 각 Player 객체에 이미지 연결 (속성 추가)
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
    
    arrived_tile = tiles[current_player.position]
    special_tile_names = ["출도", "학", "무주도", "미정"]
    add_console_message(f"{current_player.color} 플레이어가 {arrived_tile.name} 칸에 도착했습니다.")
    # 0: 출도, 5: 미정, 10: 무주도, 15: 학
    if current_player.position == 0:  # 출도 칸
        current_player.money += 2000
        add_console_message(f"{current_player.color} 플레이어가 출도 칸에 도착했습니다. 2000원을 받았습니다.")
        game_manager.turn_over()
        winner_tuple = game_manager.check_winner()
        winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
        if winner:

            add_winner_message(winner, reason)

            return False
        return True
    elif current_player.position == 5:  # 미정 칸
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
        game_manager.turn_over()
        return True
    elif current_player.position == 10:  # 무주도 칸
        current_player.stop_turns = 2
        add_console_message(f"{current_player.color} 플레이어는 무주도에 도착해 2턴간 이동할 수 없습니다.")
        game_manager.turn_over()
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
                                pass
                            else:
                                success, message = game_manager.teleport_player(player_index, idx)
                                add_console_message(message)
                                teleport_done = True
                                break
                elif event.type == pygame.QUIT:
                    return False  # 게임 종료
            # 순간이동 선택 중에도 타일 하이라이트 적용
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
        # 순간이동 후 재귀적으로 이벤트 처리
        return handle_tile_event_after_move(current_player, player_index)
    else:
        # 일반 타일(구매/업그레이드/이벤트)
        if arrived_tile.owner is None and hasattr(arrived_tile, "price") and arrived_tile.price > 0 and arrived_tile.name not in special_tile_names:
            # 소지금 부족 시 바로 메시지 출력 후 턴 넘김
            if current_player.money < arrived_tile.price:
                add_console_message(f"{current_player.color} 플레이어는 {arrived_tile.name}을(를) 구매할 돈이 부족합니다.")
                game_manager.turn_over()
                winner_tuple = game_manager.check_winner()
                winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
                if winner:

                    add_winner_message(winner, reason)

                return True
            ask_buy = True
            buy_tile_index = current_player.position
            buy_player_index = player_index
            font_btn = pygame.font.Font("board_set/font.ttf", 18)
            buy_buttons = [
                Button((60, background.get_height()-80, 80, 40), "예", font_btn),
                Button((160, background.get_height()-80, 80, 40), "아니요", font_btn)
            ]
            return True
        elif arrived_tile.owner == current_player and hasattr(arrived_tile, "price") and arrived_tile.price > 0 and arrived_tile.upgrade_level < 2:
            # 업그레이드 비용 부족 시 바로 메시지 출력 후 턴 넘김
            upgrade_cost = 500 if arrived_tile.upgrade_level == 0 else 1000
            if current_player.money < upgrade_cost:
                add_console_message(f"{current_player.color} 플레이어는 업그레이드 비용 ₩{upgrade_cost}가 부족합니다.")
                game_manager.turn_over()
                winner_tuple = game_manager.check_winner()
                winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
                if winner:

                    add_winner_message(winner, reason)

                return True
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


# 콘솔 메시지 리스트와 최대 줄 수 설정
console_messages = []  # 최근 메시지 4개 저장
MAX_CONSOLE_LINES = 8


# 콘솔 메시지 추가 함수: 새 메시지를 맨 위에 추가, 4줄 초과 시 마지막 삭제
def add_console_message(msg):
    # msg가 리스트면 각 요소를 한 줄씩 출력, 아니면 그대로 출력
    if isinstance(msg, list):
        for m in msg:
            console_messages.insert(0, str(m))
            print(str(m))
    else:
        console_messages.insert(0, str(msg))
        print(str(msg))
    # 최대 줄 수 초과 시 마지막 삭제
    while len(console_messages) > MAX_CONSOLE_LINES:
        console_messages.pop()


# 콘솔 메시지 그리기 함수: 화면 왼쪽 중앙에 최대 8줄, 폰트 크기 10, 배경 없이 텍스트만 표시
def draw_console_messages(surface):
    font = pygame.font.Font("board_set/font.ttf", 16)
    start_y = background.get_height() // 2 - (MAX_CONSOLE_LINES * 20)
    box_width = 300
    box_height = MAX_CONSOLE_LINES * 80  # 충분히 크게
    s = pygame.Surface((box_width, box_height))
    s.fill((255, 255, 255))
    surface.blit(s, (40, start_y - 2))
    max_chars = 22
    # 아래에서 위로 출력: y를 아래에서 시작해서 위로 감소
    y = start_y + (MAX_CONSOLE_LINES - 1) * 20  # 가장 아래에서 시작
    all_lines = []
    for msg in console_messages:
        lines = [msg[i:i+max_chars] for i in range(0, len(msg), max_chars)]
        all_lines.extend(lines[::-1])  # 줄바꿈된 라인을 역순으로 추가 (아래줄이 먼저 나오게)
    all_lines = all_lines[:MAX_CONSOLE_LINES]  # 최대 줄 수만큼만 출력
    for line in all_lines:
        rendered = font.render(line, True, (30, 30, 30))
        surface.blit(rendered, (45, y))  # y값을 위로 감소시키며 출력
        y -= 20  # 한 줄 위로 이동
        if y < start_y - 20:
            break  # 출력 영역을 벗어나면 중단


# --- Button 클래스 추가 ---
class Button:
    def __init__(self, rect, text, font, color=(200,200,200), text_color=(0,0,0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (100,100,100), self.rect, 2)
        rendered = self.font.render(self.text, True, self.text_color)
        text_rect = rendered.get_rect(center=self.rect.center)
        surface.blit(rendered, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# --- 구매 관련 상태 변수 ---
ask_buy = False
buy_tile_index = None
buy_player_index = None
buy_buttons = []

# --- 업그레이드 관련 상태 변수 ---
ask_upgrade = False
upgrade_tile_index = None
upgrade_player_index = None
upgrade_buttons = []


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


running = True # 실행 상태

while running: # 게임이 실행중인 동안
    clock.tick(120)

    # 파산한 플레이어의 차례는 자동으로 넘김

    # (우승자 발생 시 add_winner_message로 메시지 출력 후 running=False)
    if not skip_bankrupt_and_check_winner():  # 파산 플레이어 자동 스킵 및 우승자 발생 시 게임 종료
        break


    mouse_pos = pygame.mouse.get_pos()

    # 타일 하이라이트 및 정보 표시
    highlight_tile = None
    for tile in tiles:
        if tile.visual.rect.collidepoint(mouse_pos):
            highlight_tile = tile
            break
    for tile in tiles:
        highlight = tile.visual.rect.collidepoint(mouse_pos)
        tile.draw_owner_box(background)
        tile.visual.draw(background, tile.name, highlight)

    if highlight_tile:
        highlight_tile.draw_info(background, pos=(50, 50))
    else:
        current_tile = tiles[game_manager.get_current_player().position]
        current_tile.draw_info(background, pos=(50, 50))

    for idx, p in enumerate(game_manager.players):
        p.draw_info(background, pos=(1200, 50 + idx * 160))
    for idx in range(len(game_manager.players)):
        pygame.draw.rect(background, (255,255,255), (1195, 45 + idx*160, 260, 160), 4)
    idx = game_manager.current_player_index
    pygame.draw.rect(background, (255,0,0), (1195, 45 + idx*160, 260, 160), 4)

    # --- 플레이어 말 그리기 ---
    for idx, p in enumerate(game_manager.players):
        tile = tiles[p.position]
        # 각 타일의 player_positions에서 플레이어 turn에 맞는 위치 사용, x, y 각각 +10씩 이동
        orig_pos = tile.player_positions[p.turn]
        pos = (orig_pos[0] + 10, orig_pos[1] + 10)
        # 이미지 중앙 정렬
        img_rect = p.piece_image.get_rect(center=(int(pos[0]), int(pos[1])))
        background.blit(p.piece_image, img_rect)

    # 콘솔 메시지 그리기
    draw_console_messages(background)

    # --- 구매 질문 및 버튼 그리기 ---
    if ask_buy:
        font_q = pygame.font.Font("board_set/font.ttf", 18)
        question = font_q.render("땅을 구매하겠습니까?", True, (0,0,0))
        background.blit(question, (60, background.get_height()-120))
        for btn in buy_buttons:
            btn.draw(background)
    # --- 업그레이드 질문 및 버튼 그리기 ---
    if ask_upgrade:
        font_q = pygame.font.Font("board_set/font.ttf", 18)
        question = font_q.render("땅을 업그레이드 하시겠습니까?", True, (0,0,0))
        background.blit(question, (60, background.get_height()-180))
        for btn in upgrade_buttons:
            btn.draw(background)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif ask_buy and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 타일 구매 이벤트 처리
            for idx, btn in enumerate(buy_buttons):
                if btn.is_clicked(event.pos):
                    if idx == 0:  # 예
                        # 특수 칸(출도, 학, 무주도, 미정)은 구매 불가
                        special_tile_names = ["출도", "학", "무주도", "미정"]
                        tile = tiles[buy_tile_index]
                        if tile.name in special_tile_names:
                            add_console_message(f"{tile.name} 칸은 구매할 수 없습니다.")
                        else:
                            success, message = game_manager.buy_tile(buy_tile_index, buy_player_index)
                            add_console_message(message)
                    else:  # 아니요
                        add_console_message("구매를 취소했습니다.")
                    ask_buy = False
                    buy_tile_index = None
                    buy_player_index = None
                    buy_buttons = []
                    game_manager.turn_over()
                    # 우승자 체크
                    winner_tuple = game_manager.check_winner()
                    winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
                    if winner:

                        add_winner_message(winner, reason)  # 우승자 메시지 일관 출력 함수
                        running = False
                    break

        elif ask_upgrade and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 타일 업그레이드 이벤트 처리
            for idx, btn in enumerate(upgrade_buttons):
                if btn.is_clicked(event.pos):
                    if idx == 0:  # 예
                        success, message = game_manager.upgrade_tile(upgrade_tile_index, upgrade_player_index)
                        add_console_message(message)
                    else:
                        add_console_message("업그레이드를 취소했습니다.")
                    ask_upgrade = False
                    upgrade_tile_index = None
                    upgrade_player_index = None
                    upgrade_buttons = []
                    game_manager.turn_over()

                    # 우승자 체크
                    winner_tuple = game_manager.check_winner()
                    winner, reason = winner_tuple if isinstance(winner_tuple, tuple) else (winner_tuple, None)
                    if winner:
                        add_winner_message(winner, reason)  # 우승자 메시지 일관 출력 함수
                        running = False
                    break

        elif not ask_buy and not ask_upgrade and event.type == pygame.KEYDOWN: # 일반적인 이벤트 처리 (주사위 굴리기 및 특수 타일 이벤트)
            if event.key == pygame.K_SPACE:
                current_player = game_manager.get_current_player()
                add_console_message(f"{current_player.color} 플레이어의 턴입니다.") # 현재 플레이어 턴 메시지
                if current_player.is_bankrupt: # 파산 상태인 플레이어는 턴을 넘김
                    add_console_message(f"{game_manager.get_current_player_color()} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
                    game_manager.turn_over()
                elif getattr(current_player, 'stop_turns', 0) > 0:
                    add_console_message(f"{current_player.color} 플레이어는 이동불가 상태입니다. (남은 턴: {current_player.stop_turns})")
                    dice1, dice2 = roller.roll_two_dice(group_pos=(44, 600))
                    add_console_message(f"주사위 결과: {dice1}, {dice2}")
                    if dice1 == dice2:
                        steps = dice1 + dice2
                        current_player.move(steps)
                        add_console_message(f"두 눈이 같아 {steps}칸 이동합니다!")
                        current_player.stop_turns = 0
                        player_index = game_manager.current_player_index
                        result = handle_tile_event_after_move(current_player, player_index)
                        if result == 'exit':
                            running = False
                            break
                    else:
                        add_console_message("이동하지 못합니다.")
                        current_player.stop_turns -= 1
                        game_manager.turn_over()
                else:
                    steps = roller.roll_dice(group_pos=(44, 600))  # 주사위 위치 조정(group_pos=(좌표)), (0, 0)은 화면 좌측 상단
                    current_player.move(steps)
                    add_console_message(f"{current_player.color} 플레이어가 {steps}칸 이동했습니다.")
                    player_index = game_manager.current_player_index
                    result = handle_tile_event_after_move(current_player, player_index)
                    if result == 'exit':
                        running = False
                        break
            elif event.key == pygame.K_p and pygame.key.get_pressed()[pygame.K_F1]:
                add_console_message(f'현제 플레이어들의 위치: {[p.position for p in game_manager.players]}')
            elif event.key == pygame.K_m and pygame.key.get_pressed()[pygame.K_F1]:
                add_console_message(f'현제 플레이어들의 돈: {[p.money for p in game_manager.players]}')
            elif event.key == pygame.K_t and pygame.key.get_pressed()[pygame.K_F1]:
                selected_player_index = int(input("플레이어 인덱스를 입력하세요 (0-3): "))
                destination_tile_index = int(input("이동할 타일의 인덱스를 입력하세요 (0-19): "))
                game_manager.teleport_player(selected_player_index, destination_tile_index)
        elif not ask_buy and not ask_upgrade and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, tile in enumerate(tiles):
                if tile.is_clicked(mouse_pos):
                    add_console_message(f"{tile.name} 타일 클릭")
                    break
    pygame.display.update()

pygame.quit()
