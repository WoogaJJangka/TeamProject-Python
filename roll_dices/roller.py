import pygame
import os
import random
import time

# 🎲 주사위 클래스 정의
class DiceRoller: 
    def __init__(self, screen, image_folder_path, size=(100, 100)):
        """
        DiceRoller 클래스의 생성자.
        - screen: 주사위를 그릴 Pygame 화면 Surface 객체
        - image_folder_path: 주사위 이미지가 저장된 폴더 경로
        - size: 주사위 이미지의 크기 (기본값 100x100)
        """
        self.screen = screen  # 주사위가 그려질 화면
        self.image_folder_path = image_folder_path  # 이미지 폴더 경로
        self.size = size  # 주사위 이미지 크기 (너비, 높이)
        self.dice_imgs = self._load_dice_images()  # 1~6 주사위 눈 이미지 불러오기

    def _load_dice_images(self):
        """
        dice1.png ~ dice6.png 이미지 파일을 불러와 리스트로 반환.
        이미지 크기는 self.size로 조정됨.
        """
        imgs = []
        for i in range(1, 7):  # 주사위 눈 1~6
            img_path = os.path.join(self.image_folder_path, f"dice{i}.png")  # 이미지 파일 경로 생성
            img = pygame.image.load(img_path)  # 이미지 파일 로드
            img = pygame.transform.scale(img, self.size)  # 이미지 크기 조정
            imgs.append(img)  # 리스트에 추가
        return imgs  # 이미지 리스트 반환

    def roll_two_dice(self, group_pos=None, roll_times=20, delay=50):
        """
        두 개의 주사위를 동시에 굴리는 함수. 애니메이션 포함.
        - group_pos: 주사위 객체 그룹(배경 포함)의 좌상단 위치 (지정하지 않으면 화면 중앙)
        - roll_times: 주사위가 굴러가는 애니메이션 프레임 수
        - delay: 각 프레임 간 지연 시간 (ms 단위)
        """
        dice_w, dice_h = self.size  # 주사위 이미지 너비, 높이
        gap = 40  # 주사위 사이 간격
        pad = 20  # 배경 여백

        # 배경판과 주사위 전체 그룹의 위치 및 크기 계산
        if group_pos is None:
            # 위치가 주어지지 않았을 경우: 화면 중앙에 배치
            screen_w, screen_h = self.screen.get_size()
            total_w = dice_w * 2 + gap  # 두 주사위 + 간격
            bg_rect_width = total_w + pad * 2
            bg_rect_height = dice_h + pad * 2
            bg_rect_x = (screen_w - bg_rect_width) // 2
            bg_rect_y = (screen_h - bg_rect_height) // 2
        else:
            # 위치가 지정된 경우 해당 위치 사용
            bg_rect_x, bg_rect_y = group_pos
            total_w = dice_w * 2 + gap
            bg_rect_width = total_w + pad * 2
            bg_rect_height = dice_h + pad * 2

        # 각 주사위의 실제 그려질 위치 계산
        pos1 = (bg_rect_x + pad, bg_rect_y + pad)  # 첫 번째 주사위 위치
        pos2 = (bg_rect_x + pad + dice_w + gap, bg_rect_y + pad)  # 두 번째 주사위 위치

        idx1 = idx2 = 0  # 주사위 눈 인덱스 초기값

        for _ in range(roll_times):
            # 주사위 눈 랜덤 설정 (0~5)
            idx1 = random.randint(0, 5)
            idx2 = random.randint(0, 5)

            # 배경 외곽 검은색 테두리
            pygame.draw.rect(
                self.screen, (0, 0, 0),
                (bg_rect_x - 3, bg_rect_y - 3, bg_rect_width + 6, bg_rect_height + 6),
                border_radius=24
            )
            # 흰색 배경판
            pygame.draw.rect(
                self.screen, (255, 255, 255),
                (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height),
                border_radius=20
            )

            # 두 주사위 눈 이미지 출력
            self.screen.blit(self.dice_imgs[idx1], pos1)
            self.screen.blit(self.dice_imgs[idx2], pos2)
            pygame.display.update()  # 화면 업데이트
            pygame.time.delay(delay)  # 프레임 간 딜레이

        # 🎯 마지막으로 나온 주사위 눈을 다시 그려서 고정
        pygame.draw.rect(
            self.screen, (0, 0, 0),
            (bg_rect_x - 3, bg_rect_y - 3, bg_rect_width + 6, bg_rect_height + 6),
            border_radius=24
        )
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height),
            border_radius=20
        )
        self.screen.blit(self.dice_imgs[idx1], pos1)
        self.screen.blit(self.dice_imgs[idx2], pos2)
        pygame.display.update()
        time.sleep(1)  # 1초 동안 결과를 보여줌
        return idx1 + 1, idx2 + 1 # 실제 주사위 눈(1~6) 반환