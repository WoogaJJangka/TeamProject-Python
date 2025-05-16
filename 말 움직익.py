import turtle as tt
import random as rd
import time

tt.shape("circle")
tt.penup()
tt.speed(0)

class set_horse:    # 말 처음 설정
    def __init__(self, x, y, color,name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name

    def first_set(self):
        tt.color(self.color)
        tt.goto(self.x, self.y)
        tt.stamp()

def move(horse_num, value):
    if horse_num == horse_data.index(redh):
        tt.goto(redh.x,redh.y)
        redh.y += value
        tt.speed(1)
        tt.clearstamps(1)
        redh.first_set()

    if horse_num == horse_data.index(blueh):
        tt.goto(blueh.x,blueh.y)
        blueh.y += value
        tt.speed(1)
        tt.clearstamps(1)
        blueh.first_set()

    if horse_num == horse_data.index(greenh):
        tt.goto(greenh.x,greenh.y)
        greenh.y += value
        tt.speed(1)
        tt.clearstamps(1)
        greenh.first_set()

    if horse_num == horse_data.index(yellowh):
        tt.goto(yellowh.x,yellowh.y)
        yellowh.y += value
        tt.speed(1)
        tt.clearstamps(1)
        yellowh.first_set()



redh = set_horse(190,-190,"red","빨강말")
blueh = set_horse(210,-210,"blue","파랑말")
greenh = set_horse(190,-210,"green","초록말")
yellowh = set_horse(210,-190,"yellow","노랑말")


horse_data = [redh, blueh, greenh, yellowh]
rd.shuffle(horse_data)


horse_name = []
for horse_n in horse_data:
    horse_name.append(horse_n.name)

first_horse_num = "True"
tt.goto(-110, 0)

for i in horse_name:

    if first_horse_num == "True":
        tt.write(i,font=("굴림체",50))
        tt.goto(-130,-50)
    else:
        tt.write(i,font=("굴림체",15))
        tt.fd(90)
    first_horse_num = "False"


for horse_first_pos in horse_data:
    horse_first_pos.first_set()



time.sleep(5)
while True:
    horse_num = 0
    for horse in horse_data:
        distance = tt.textinput("거리", "입력")
        tt.speed(0)
        move(horse_num, int(distance) * 40)
        horse_num += 1
