import pygame

if __name__ == "__main__": # background 빨간 줄 해결 코드
    background = pygame.display.set_mode((1500,1000))


class TileDeco:  # 타일 설정하기 클래스
    def __init__(self, name, name_size, name_position, mouse_position, horse_position): # 초기 설정

        self.name = name # 타일 이름
        self.name_size = name_size # 타일 이름 크기
        self.name_position = name_position # 타일 이름 위치

        self.mouse_position = mouse_position # 마우스 위치 감지
        self.color = "yellow" # 타일 노란색

        self.horse_position = horse_position # 말 위치 4개로 튜플로 나눌 예정


    def tile_word(self,background): # 하얀 배경 검은 글씨 써 넣는 메서드
        pygame.draw.rect(background, (255, 255, 255), self.mouse_position, 100)
        font = pygame.font.Font("board_set/font.ttf", self.name_size)
        font = font.render(self.name, True, (0, 0, 0))
        background.blit(font, self.name_position)

    def tile_cog_color(self,background): # 타일 노란색을 바꾸기 메서드
        pygame.draw.rect(background, self.color, self.mouse_position, 100)
        font = pygame.font.Font("board_set/font.ttf", self.name_size)
        font = font.render(self.name, True, (0, 0, 0))
        background.blit(font, self.name_position)


def all_local(): # 모든 타일 함수 리스트 반환

    t1 = TileDeco("북한산성", 25, (1055, 670), (1051, 627, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t2 = TileDeco("성균관", 30, (1055, 545), (1051, 502, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t3 = TileDeco("숭례문", 30, (1055, 420), (1051, 377, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t4 = TileDeco("병산서원", 25, (1055, 300), (1051, 253, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t6 = TileDeco("숙정문", 30, (895, 135), (877, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t7 = TileDeco("종묘", 35, (780, 130), (753, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t8 = TileDeco("해인사", 30, (645, 135), (628, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t9 = TileDeco("돈의문", 30, (520, 135), (503, 103, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t11 = TileDeco("경회루", 30, (360, 295), (353, 253, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t12 = TileDeco("수원화성", 25, (355, 420), (353, 377, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t13 = TileDeco("흥인지문", 25, (355, 545), (353, 502, 96, 121), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t14 = TileDeco("남한산성", 25, (355, 670), (353, 627, 96, 120), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t16 = TileDeco("덕수궁", 30, (520, 830), (503, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t17 = TileDeco("창경궁", 30, (645, 830), (628, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t18 = TileDeco("창덕궁", 30, (770, 830), (753, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t19 = TileDeco("경복궁", 30, (895, 830), (877, 801, 120, 96), ((0, 0), (0, 0), (0, 0), (0, 0)))

    t0 = TileDeco("출도", 45, (1030, 800), (1000, 750, 147, 147), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t5 = TileDeco("학", 45, (1050, 150), (1000, 103, 147, 147), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t10 = TileDeco("무주도", 45, (360, 150), (353, 103, 147, 147), ((0, 0), (0, 0), (0, 0), (0, 0)))
    t15 = TileDeco("미정", 45, (380, 800), (353, 750, 147, 147), ((0, 0), (0, 0), (0, 0), (0, 0)))

    all_local = [t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19]

    return all_local


