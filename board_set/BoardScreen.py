import pygame

def BoardScreen(background): # 보드판 배경 그리기

    # 큰 사각형 3 개 그리기

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
            pygame.draw.line(background,(0,0,0),(625 + 125 * i,250 + 647 * j),(625 + 125 * i,100 + 650 * j),3)

    for j in range(2):  # 세로칸 그리기
        for i in range(3):
            pygame.draw.line(background, (0, 0, 0), (350 + 650 * j,375 + 125 * i), (500 + 647 * j,375 + 125 * i), 3)


    # 한반도 사진 넣기

    img_han = pygame.image.load("board_set/한반도.png") # 한반도 사진 불러오기
    img_han = pygame.transform.scale(img_han,(200,400)) # 사진 크기 조정
    background.blit(img_han,(650,300)) # 사진 위치 조정

    # 게임 판에 중앙 글씨 넣기(조선 유람)
    font = pygame.font.Font("board_set/font.ttf", 60)  # 폰트, 크기 조정

    rendered1 = font.render("조선", True, (0, 0, 0))  # 조선 색깔
    rendered2 = font.render("유람", True, (0, 0, 0))  # 유람 색깔

    background.blit(rendered1, (695, 440))  # 조선 글자 위치 조정
    background.blit(rendered2, (695, 505))  # 유람 글자 위치 조정

