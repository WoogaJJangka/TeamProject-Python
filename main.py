
# from board_set import board_start
# import roll_dices.roller
# import pygame
#
# board_start.set_board()
# roller = roll_dices.roller.DiceRoller(board_start.background,"roll_dices\\assets")
#
# for event in pygame.event.get():
#     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # 키를 누르고 이벤트 키가 스페이스이면
#         roller.roll_dice()

import pygame
import pygame_gui
import os
from board_set.BoardScreen import BoardScreen
from roll_dices.roller import DiceRoller
from game.tile_info import all_tiles  # 개선된 all_tiles 사용
import game.game_manager as gm
import game.player as player


pygame.init()
clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))


# 보드 배경 그리기
BoardScreen(background)


# 타일 설정
tiles = all_tiles()

# 주사위 객체 생성
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))

# 플레이어 객체 생성
game_manager = gm.GameManager()

running = True
while running:
    time_delta = clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    # 타일 하이라이트
    for tile in tiles: # 타일 정보 전부 반복
        tile.draw(background, mouse_pos)
        if tile.visual.rect.collidepoint(mouse_pos):  # highlight 기준
            tile.draw_info(background, pos=(50, 50))
            break  # 하나만 표시하면 되므로 break

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 게임 X 종료
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_manager.get_current_player().is_bankrupt:
                    print(f"{game_manager.get_current_player_color()} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
                    game_manager.turn_over()
                else:
                    steps = roller.roll_dice() # 주사위 굴리기 이동 할 칸 받기
                    current_player = game_manager.get_current_player() # 현재 플레이어 객체 받기
                    current_player.move(steps) # 플레이어 이동
                    # 이동 로그 출력
                    print(f"{current_player.color} 플레이어가 {steps}칸 이동했습니다.")
                    print(f"현재 위치: {current_player.position}")
                    # 타일 이벤트 처리
                    if current_player.position == 5:
                        print(f"{current_player.color} 플레이어가 학 타일에 도착했습니다.")
                        succes, message = game_manager.teleport_player(current_player.turn, 0)
                        print(message)
                        game_manager.turn_over()  # 턴 넘기기
                    else:
                        succes, message = game_manager.tile_event(current_player.position, current_player.turn)
                        print(message)
                        game_manager.turn_over()  # 턴 넘기기

            # F1 + p (커맨드)
            elif event.key == pygame.K_p:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F1]:
                    print(f'현제 플레이어들의 위치: {[p.position for p in game_manager.players]}')
                
            # F1 + m (커맨드)
            elif event.key == pygame.K_m:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F1]:
                    print(f'현제 플레이어들의 돈: {[p.money for p in game_manager.players]}')
                    
            # F1 + t (커맨드)
            elif event.key == pygame.K_t:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F1]:
                    selected_player_index = int(input("플레이어 인덱스를 입력하세요 (0-3): "))
                    destination_tile_index = int(input("이동할 타일의 인덱스를 입력하세요 (0-19): "))
                    game_manager.teleport_player(selected_player_index, destination_tile_index)


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, tile in enumerate(tiles): # 0부터 19까지 타일 반복(인덱스 번호, 타일)
                if tile.is_clicked(mouse_pos): # 특정 타일과 마우스 포인터가 겹칠 경우 True
                    print(idx)
                    break


    pygame.display.update()

pygame.quit()
