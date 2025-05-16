import random # 랜덤 모듈을 불러옴

def roll_dice(): # 주사위 굴리기기
        d1, d2 = random.randint(1, 6), random.randint(1, 6) # 주사위 2개를 굴림
        print(f"주사위 결과: {d1}, {d2}") # 주사위 결과 출력
        if d1 == d2: # 만약 주사위 2개가 같으면
            return d1 + d2 + roll_dice() # 다시 주사위를 굴림
        else:
              print(d1, d2)
        return d1 + d2

