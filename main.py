import pygame
import os
from board_set.BoardScreen import BoardScreen
from roll_dices.roller import DiceRoller
from game.tile_info import all_tiles
import game.game_manager as gm
import game.player as player

pygame.init()
clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))

# 보드 배경 그리기
BoardScreen(background)

# 타일 및 객체 생성
tiles = all_tiles()
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))
game_manager = gm.GameManager()


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
            p.draw_info(background, pos=(1200, 50 + idx * 160))
        pygame.display.update()
    return True


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
        if tile is highlight_tile:
            tile.visual.draw(background, tile.name, highlight=True)
        else:
            tile.visual.draw(background, tile.name, highlight=False)
    if highlight_tile:
        highlight_tile.draw_info(background, pos=(50, 50))

    # 플레이어 정보 패널 그리기
    for idx, p in enumerate(game_manager.players):
        p.draw_info(background, pos=(1200, 50 + idx * 160))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_player = game_manager.get_current_player()
                if current_player.is_bankrupt:
                    print(f"{game_manager.get_current_player_color()} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
                    game_manager.turn_over()
                else:
                    steps = roller.roll_dice()
                    current_player.move(steps)
                    print(f"{current_player.color} 플레이어가 {steps}칸 이동했습니다.")
                    print(f"현재 위치: {current_player.position}")
                    player_index = current_player.turn - 1
                    if current_player.position == 15:
                        if not handle_teleport(current_player, player_index):
                            running = False
                            break
                        success, message = game_manager.tile_event(current_player.position, player_index)
                        print(message)
                        game_manager.turn_over()
                    else:
                        success, message = game_manager.tile_event(current_player.position, player_index)
                        print(message)
                        game_manager.turn_over()
            # F1 + p (커맨드)
            elif event.key == pygame.K_p and pygame.key.get_pressed()[pygame.K_F1]:
                print(f'현제 플레이어들의 위치: {[p.position for p in game_manager.players]}')
            # F1 + m (커맨드)
            elif event.key == pygame.K_m and pygame.key.get_pressed()[pygame.K_F1]:
                print(f'현제 플레이어들의 돈: {[p.money for p in game_manager.players]}')
            # F1 + t (커맨드)
            elif event.key == pygame.K_t and pygame.key.get_pressed()[pygame.K_F1]:
                selected_player_index = int(input("플레이어 인덱스를 입력하세요 (0-3): "))
                destination_tile_index = int(input("이동할 타일의 인덱스를 입력하세요 (0-19): "))
                game_manager.teleport_player(selected_player_index, destination_tile_index)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, tile in enumerate(tiles):
                if tile.is_clicked(mouse_pos):
                    print(idx)
                    break

    pygame.display.update()

pygame.quit()
