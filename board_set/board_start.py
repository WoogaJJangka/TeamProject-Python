import pygame
import BoardScreen as BS # 뒷배경 함수 불러오기
from Tile import Tile
from roll_dices import roller

pygame.init()


clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))

BS.BoardScreen(background) # 뒷배경 그리기 함수 실행

# 타일 설정
# 지역 칸 설정
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
# 이벤트 칸 설정
et_출도 = Tile("출도", 45, (1030, 800), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))
et_무주도 = Tile("무주도", 45, (360, 150), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))
et_학 = Tile("학", 45, (1050, 150), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))
et_미정 = Tile("미정", 45, (380, 800), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)))

# 설정된 타일 리스트
all_local = [et_출도, t_북한산성, t_성균관, t_숭례문, t_병산서원, et_학, t_숙정문, t_종묘, t_해인사, t_돈의문, et_무주도 , t_경회루, t_수원화성, t_흥인지문, t_남한산성, et_미정, t_덕수궁,
             t_창경궁, t_창덕궁, t_경복궁]

# 보드판에 글씨 반복해서 써 넣기
for name in all_local:
    Tile.tile_word(name,background)



# 게임 실행
def set_board():

    done = True
    while done:
        clock.tick(60)

        mouse_pos = pygame.mouse.get_pos() # 마우스 좌표 변수

        for event in pygame.event.get(): # 창 X 게임 종료
            if event.type == pygame.QUIT:
                done = False


            for m_p in all_local: # 마우스 포인터 지역 감지

                rect = pygame.Rect(m_p.mouse_position) # 영역 위치 및 넓이

                if rect.collidepoint(mouse_pos): # 참이면 칸 배경 노란색으로
                    m_p.tile_cog_color(background)

                else: # 거짓이면 하얀색배경에 검은 글씨로
                    m_p.tile_word(background)

                roller = roller.DiceRoller(background,"roll_dices\\assets")

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # 키를 누르고 이벤트 키가 스페이스이면
                        roller.roll_dice()


        pygame.display.update()

    pygame.quit()