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
import os
from board_set.BoardScreen import BoardScreen
from board_set.Tile import Tile
from roll_dices.roller import DiceRoller

pygame.init()
clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))

# 보드 배경 그리기
BoardScreen(background)

# 타일 설정 (board_set/board_start.py 참고)
t_북한산성 = Tile("북한산성", 25, (1055, 670), (1051, 627, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_성균관 = Tile("성균관", 30, (1055, 545), (1051, 502, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_숭례문 = Tile("숭례문", 30, (1055, 420), (1051, 377, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_병산서원 = Tile("병산서원", 25, (1055, 300), (1051, 253, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_숙정문 = Tile("숙정문", 30, (895, 135), (877, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_종묘 = Tile("종묘", 35, (780, 130), (753, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_해인사 = Tile("해인사", 30, (645, 135), (628, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_돈의문 = Tile("돈의문", 30, (520, 135), (503, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_경회루 = Tile("경회루", 30, (360, 295), (353, 253, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_수원화성 = Tile("수원화성", 25, (355, 420), (353, 377, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_흥인지문 = Tile("흥인지문", 25, (355, 545), (353, 502, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_남한산성 = Tile("남한산성", 25, (355, 670), (353, 627, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_덕수궁 = Tile("덕수궁", 30, (520, 830), (503, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_창경궁 = Tile("창경궁", 30, (645, 830), (628, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_창덕궁 = Tile("창덕궁", 30, (770, 830), (753, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
t_경복궁 = Tile("경복궁", 30, (895, 830), (877, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
et_출도 = Tile("출도", 45, (1030, 800), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))
et_무주도 = Tile("무주도", 45, (360, 150), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))
et_학 = Tile("학", 45, (1050, 150), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))
et_미정 = Tile("미정", 45, (380, 800), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))

all_local = [et_출도, t_북한산성, t_성균관, t_숭례문, t_병산서원, et_학, t_숙정문, t_종묘, t_해인사, t_돈의문, et_무주도 , t_경회루, t_수원화성, t_흥인지문, t_남한산성, et_미정, t_덕수궁,
             t_창경궁, t_창덕궁, t_경복궁]

# 타일 글씨 그리기
for name in all_local:
    Tile.tile_word(name, background)

# 주사위 객체 생성
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))

running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # 스페이스바 누르면 주사위 굴리기
            roller.roll_dice()

    # 마우스가 타일 위에 있으면 색상 변경
    for m_p in all_local:
        rect = pygame.Rect(m_p.mouse_position)
        if rect.collidepoint(mouse_pos):
            m_p.tile_cog_color(background)
        else:
            m_p.tile_word(background)

    pygame.display.update()

pygame.quit()

