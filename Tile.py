import pygame

if __name__ == "__main__": # 따로 확인 하기 위한 코드
    background = pygame.display.set_mode((1500,1000))
    background.fill((255,255,255))

    pygame.init()



class Tile:  # 타일 설정하기 클래스
    def __init__(self, name, name_size, name_position, mouse_position, horse_position, tile_price): # 초기 설정

        self.name = name # 타일 이름
        self.name_size = name_size # 타일 이름 크기
        self.name_position = name_position # 타일 이름 위치

        self.mouse_position = mouse_position # 마우스 위치 감지
        self.color = "yellow" # 타일 노란색

        self.horse_position = horse_position # 말 위치 4개로 튜플로 나눌 예정

        self.onwer = None # 땅 주인 여부

        self.tile_price = tile_price # 땅 가격

        # 통행료
        # 이벤트 지역은 무한대라서 무한대 오류 남
        # 이벤트 지역 통행료만 0으로 만들기
        try:
            self.tile_toll = int(self.tile_price) * 1.0
        except: self.tile_toll = 0

        self.tile_level = 0 # 타일 첫 레벨 설정


    def tile_word(self,background): # 글씨 써 넣는 메서드

        font = pygame.font.Font("font.ttf", self.name_size)
        font = font.render(self.name, True, (0, 0, 0))
        background.blit(font, self.name_position)




if __name__ == "__main__": # 따로 확인하기 위한 코드

    t_북한산성 = Tile("북한산성", 25, (1055, 670), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_성균관 = Tile("성균관", 30, (1055, 545), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_숭례문 = Tile("숭례문", 30, (1055, 420), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_병산서원 = Tile("병산서원", 25, (1055, 300), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_숙정문 = Tile("숙정문", 30, (895, 135), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_종묘 = Tile("종묘", 35, (780, 130), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_해인사 = Tile("해인사", 30, (645, 135), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_돈의문 = Tile("돈의문", 30, (520, 135), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_경회루 = Tile("경회루", 30, (360, 295), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_수원화성 = Tile("수원화성", 25, (355, 420), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_흥인지문 = Tile("흥인지문", 25, (355, 545), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_남한산성 = Tile("남한산성", 25, (355, 670), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_덕수궁 = Tile("덕수궁", 30, (520, 830), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_창경궁 = Tile("창경궁", 30, (645, 830), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_창덕궁 = Tile("창덕궁", 30, (770, 830), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)
    t_경복궁 = Tile("경복궁", 30, (895, 830), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), 0)

    et_출도 = Tile("출도", 45, (1030, 800), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), float("inf"))
    et_무주도 = Tile("무주도", 45, (360, 150), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), float("inf"))
    et_학 = Tile("학", 45, (1050, 150), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), float("inf"))
    et_미정 = Tile("미정", 45, (380, 800), (0, 0, 0, 0), ((0, 0), (0, 0), (0, 0), (0, 0)), float("inf"))

    all_local = [t_북한산성, t_성균관, t_숭례문, t_병산서원, t_숙정문, t_종묘, t_해인사, t_돈의문, t_경회루, t_수원화성, t_흥인지문, t_남한산성, t_덕수궁,
                 t_창경궁, t_창덕궁, t_경복궁]




    for i in all_local:
        i.tile_word(background)

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.update()


    pygame.quit()
