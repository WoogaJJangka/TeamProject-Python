import pygame

def BoardScreen(): # 보드판 그리기

    #하얀색 배경 꺼내기
    background = pygame.display.set_mode((1500,1000))
    background.fill((255,255,255))

    # 큰 도형 3 개 그리기
    pygame.draw.rect(background, (0, 0, 0), (500, 250, 500, 500), 3)
    pygame.draw.rect(background, (0, 0, 0), (450, 200, 600, 600), 3)
    pygame.draw.rect(background, (0, 0, 0), (350, 100, 800, 800), 3)

    # 이벤트 지역에 넘어간 검은 선 지우기
    pygame.draw.rect(background, (255,255,255), (350, 100, 153, 153), 99)
    pygame.draw.rect(background, (255,255,255), (997, 100, 153, 153), 99)
    pygame.draw.rect(background, (255,255,255), (350, 747, 153, 153), 99)
    pygame.draw.rect(background, (255,255,255), (997, 747, 153, 153), 99)

    # 이벤트 지역 다시 그리기
    pygame.draw.rect(background, (0, 0, 0), (350, 100, 153, 153), 3)
    pygame.draw.rect(background, (0, 0, 0), (997, 100, 153, 153), 3)
    pygame.draw.rect(background, (0, 0, 0), (350, 747, 153, 153), 3)
    pygame.draw.rect(background, (0, 0, 0), (997, 747, 153, 153), 3)

    # 지역 나누는 선 그리기
    for j in range(2): # 가로칸 그리기
        for i in range(3):
            pygame.draw.line(background,(0,0,0),(625 + 125 * i,250 + 650 * j),(625 + 125 * i,100 + 650 * j),3)

    for j in range(2):  # 세로칸 그리기
        for i in range(3):
            pygame.draw.line(background, (0, 0, 0), (350 + 650 * j,375 + 125 * i), (500 + 650 * j,375 + 125 * i), 3)