import random # 랜덤 모듈을 불러옴

def roll_dice(): # 주사위 굴리기기
        d1, d2 = random.randint(1, 6), random.randint(1, 6) # 주사위 2개를 굴림
        step = (d1 + d2)
        print(f"주사위 결과: {d1}, {d2}") # 주사위 결과 출력
        print(step , 0)
        while d1 == d2:
                d1 , d2 = random.randint(1, 6), random.randint(1, 6) # 주사위 2개를 굴림
                print(f"주사위 결과: {d1}, {d2}") # 주사위 결과 출력
                step += (d1 + d2)
                print (step ,1)
        return step

roll_dice()