import pygame
from roller import DiceRoller

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("두 개의 주사위 굴리기")
clock = pygame.time.Clock()

roller = DiceRoller(screen, "assets")  # 이미지 폴더 경로

running = True
while running:
    screen.fill((255, 255, 255))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            result1, result2 = roller.roll_two_dice()
            print(f"🎲 주사위 결과: {result1}, {result2}")

    clock.tick(60)

pygame.quit()
