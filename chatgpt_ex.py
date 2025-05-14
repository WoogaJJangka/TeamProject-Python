import tkinter as tk
from PIL import Image, ImageTk

# 기본 설정
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# 각 칸의 좌표 (예: 6칸짜리 보드 가정)
tile_coords = [
    (50, 700),  # 0번 칸 (출발)
    (150, 700),
    (250, 700),
    (350, 700),
    (450, 700),
    (550, 700)
]

# 플레이어 클래스
class Player:
    def __init__(self, name, token_img, canvas):
        self.name = name
        self.position = 0
        self.canvas = canvas
        self.image = token_img
        self.token = canvas.create_image(*tile_coords[0], image=self.image, anchor='center')

    def move(self, steps):
        self.position = (self.position + steps) % len(tile_coords)
        new_x, new_y = tile_coords[self.position]
        self.canvas.coords(self.token, new_x, new_y)

# 주창 생성
root = tk.Tk()
root.title("부루마블")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# 캔버스 생성
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

# 이미지 불러오기
board_img = Image.open("board.png")  # 너가 가진 보드 이미지 경로
board_img = board_img.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
board_tk = ImageTk.PhotoImage(board_img)
canvas.create_image(0, 0, anchor='nw', image=board_tk)

# 말 이미지 불러오기
player_img_raw = Image.open("player1.png").resize((50, 50))
player_img = ImageTk.PhotoImage(player_img_raw)

# 플레이어 객체 생성
player = Player("Player 1", player_img, canvas)

# 주사위 굴리기 버튼 기능
import random
def roll_dice():
    steps = random.randint(1, 6)
    print(f"주사위: {steps}")
    player.move(steps)

# 버튼 추가
button = tk.Button(root, text="주사위 굴리기", command=roll_dice)
button.pack()

# 메인 루프 시작
root.mainloop()
