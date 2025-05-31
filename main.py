import pygame
import os
from board_set.BoardScreen import BoardScreen
from roll_dices.roller import DiceRoller
from game.tile_info import all_tiles
import game.game_manager as gm
import game.player as player

print("게임 시작1")
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


def handle_teleport(current_player, player_index):
    print(f"{current_player.color} 플레이어가 학 타일에 도착했습니다.")
    teleport_done = False
    while not teleport_done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for idx, tile in enumerate(tiles):
                    if tile.is_clicked(mouse_pos):
                        if idx == 15:
                            print("학 타일로는 순간이동할 수 없습니다.")
                        else:
                            print(f"{idx}번 타일로 순간이동 시도")
                            success, message = game_manager.teleport_player(player_index, idx)
                            print(message)
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
            # 플레이어 인덱스와 색상 정보 표시 (디버깅용)
            print(f"[DEBUG] idx={idx}, turn={p.turn}, color={p.color}, pos={p.position}, properties={[t.name for t in p.properties]}")
            p.draw_info(background, pos=(1200, 50 + idx * 160))
        pygame.display.update()
    return True


# 콘솔 메시지 리스트와 최대 줄 수 설정
console_messages = []  # 최근 메시지 4개 저장
MAX_CONSOLE_LINES = 8


# 콘솔 메시지 추가 함수: 새 메시지를 맨 위에 추가, 4줄 초과 시 마지막 삭제
def add_console_message(msg):
    console_messages.insert(0, str(msg))
    if len(console_messages) > MAX_CONSOLE_LINES:
        console_messages.pop()


# 콘솔 메시지 그리기 함수: 화면 왼쪽 중앙에 최대 8줄, 폰트 크기 10, 배경 없이 텍스트만 표시
def draw_console_messages(surface):
    font = pygame.font.Font("board_set/font.ttf", 10)
    # 화면 왼쪽 중앙에 정렬
    start_y = background.get_height() // 2 - (MAX_CONSOLE_LINES * 20)
    box_width = 290
    box_height = MAX_CONSOLE_LINES * 80  # 충분히 크게
    # 메시지 영역을 완전히 흰색으로 clear (알파값 255, 완전 불투명)
    s = pygame.Surface((box_width, box_height))
    s.fill((255, 255, 255))
    surface.blit(s, (40, start_y - 2))
    # 메시지 텍스트만 그림 (한 줄이 너무 길면 줄바꿈)
    max_chars = 30
    y = start_y
    for msg in console_messages:
        lines = [msg[i:i+max_chars] for i in range(0, len(msg), max_chars)]
        for line in lines:
            rendered = font.render(line, True, (30, 30, 30))
            surface.blit(rendered, (45, y))
            y += 20


running = True
while running:
    time_delta = clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    # 타일 하이라이트 및 정보 표시
    highlight_tile = None
    for tile in tiles:
        if tile.visual.rect.collidepoint(mouse_pos):
            highlight_tile = tile
            break
    for tile in tiles:
        highlight = tile.visual.rect.collidepoint(mouse_pos)
        # 1. empty_rect에 소유자 색 네모를 먼저 그림 (draw_owner_box가 흰색/소유자색 모두 처리)
        tile.draw_owner_box(background)
        # 2. empty_rect에 흰색 네모를 덮지 않음 (중복 제거)
        # 3. 타일 본체를 항상 마지막에 그림 (이름 등은 위에 오도록)
        tile.visual.draw(background, tile.name, highlight)

    # 반드시 타일 정보 박스가 보이게!
    if highlight_tile:
        highlight_tile.draw_info(background, pos=(50, 50))
    else:
        # 마우스가 아무 타일에도 없을 때, 현재 플레이어의 위치 타일 정보를 표시
        current_tile = tiles[game_manager.get_current_player().position]
        current_tile.draw_info(background, pos=(50, 50))

    # 플레이어 정보 패널 그리기 (draw_info 먼저)
    for idx, p in enumerate(game_manager.players):
        p.draw_info(background, pos=(1200, 50 + idx * 160))
    # 모든 패널 위에 흰색 테두리로 덮어서 기존 테두리 완전 제거
    for idx in range(len(game_manager.players)):
        pygame.draw.rect(background, (255,255,255), (1195, 45 + idx*160, 260, 160), 4)
    # 자신의 차례인 패널에만 빨간 테두리
    idx = game_manager.current_player_index
    pygame.draw.rect(background, (255,0,0), (1195, 45 + idx*160, 260, 160), 4)

    # 콘솔 메시지 그리기
    draw_console_messages(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_player = game_manager.get_current_player()
                if current_player.is_bankrupt:
                    add_console_message(f"{game_manager.get_current_player_color()} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
                    game_manager.turn_over()
                else:
                    steps = roller.roll_dice()
                    current_player.move(steps)
                    add_console_message(f"{current_player.color} 플레이어가 {steps}칸 이동했습니다.")
                    print(f"현재 위치: {current_player.position}")
                    player_index = game_manager.current_player_index  # 현재 턴 인덱스를 직접 사용
                    # 이동 후 도착 메시지 추가
                    arrived_tile = tiles[current_player.position]
                    add_console_message(f"{current_player.color} 플레이어가 {arrived_tile.name} 칸에 도착했습니다.")
                    if current_player.position == 15:
                        add_console_message("학 칸에 도착했습니다! 원하는 타일을 클릭해 이동하세요.")
                        draw_console_messages(background)
                        pygame.display.update()
                        if not handle_teleport(current_player, player_index):
                            running = False
                            break
                        success, message = game_manager.tile_event(current_player.position, player_index)
                        add_console_message(message)
                        game_manager.turn_over()
                    else:
                        success, message = game_manager.tile_event(current_player.position, player_index)
                        add_console_message(message)
                        game_manager.turn_over()
                        
            # F1 + p (커맨드)
            elif event.key == pygame.K_p and pygame.key.get_pressed()[pygame.K_F1]:
                add_console_message(f'현제 플레이어들의 위치: {[p.position for p in game_manager.players]}')
            # F1 + m (커맨드)
            elif event.key == pygame.K_m and pygame.key.get_pressed()[pygame.K_F1]:
                add_console_message(f'현제 플레이어들의 돈: {[p.money for p in game_manager.players]}')
            # F1 + t (커맨드)
            elif event.key == pygame.K_t and pygame.key.get_pressed()[pygame.K_F1]:
                selected_player_index = int(input("플레이어 인덱스를 입력하세요 (0-3): "))
                destination_tile_index = int(input("이동할 타일의 인덱스를 입력하세요 (0-19): "))
                game_manager.teleport_player(selected_player_index, destination_tile_index)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, tile in enumerate(tiles):
                if tile.is_clicked(mouse_pos):
                    add_console_message(f"{tile.name} 타일 클릭")
                    break
    pygame.display.update()

pygame.quit()