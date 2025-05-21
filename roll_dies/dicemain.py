import pygame
import random 
from roll_dies.roller import DiceRoller


pygame.init() # 파이게임 초기화
screen = pygame.display.set_mode((400, 300)) # 스크린 크기 설정
pygame.display.set_caption("두 개의 주사위 굴리기") # 파이게임 창 캡션 설정
clock = pygame.time.Clock() # 시간 변수 설정

roller = DiceRoller(screen, "roll_dies\\assets")  # 이미지 폴더 경로

def roll_dice(): # 주사위 굴리기기
        result1 , result2 = roller.roll_two_dice() # 2개의 주사위 결과를 받기
        print(f"🎲 주사위 결과: {result1}, {result2}") # 결과를 터미널에 표시
        step = (result1 + result2)
        print(step , 0)
        while result1 == result2:
                result1 , result2 = roller.roll_two_dice()
                print(f"🎲 주사위 결과: {result1}, {result2}") # 결과를 터미널에 표시
                step += (result1 + result2)
                print (step ,1)
        return step
        

running = True # 작동 상태
while running:
    screen.fill((255, 255, 255)) #스크린을 흰색으로 채움
    pygame.display.update() #스크린 업데이트(적용)

    for event in pygame.event.get(): # 이벤트 감지
        if event.type == pygame.QUIT: # 파이게임이 종료되면
            running = False # 작동 종료 상태

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # 키를 누르고 이벤트 키가 스페이스이면
            roll_dice()

    clock.tick(60) # 프레임 60으로 설정

pygame.quit()
