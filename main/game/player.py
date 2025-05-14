<<<<<<< HEAD
class Player:
    def __init__(self, pid, color):
        self.id = pid
        self.color = color  # 'red', 'blue', etc
        self.money = 5000
        self.position = 0
        self.properties = []
        self.is_bankrupt = False

    def move(self, steps, board_size):
        self.position = (self.position + steps) % board_size

    def pay(self, amount):
        self.money -= amount
        if self.money < 0:
            return False
=======
class Player:
    def __init__(self, pid, color):
        self.id = pid
        self.color = color  # 'red', 'blue', etc
        self.money = 5000
        self.position = 0
        self.properties = []
        self.is_bankrupt = False

    def move(self, steps, board_size):
        self.position = (self.position + steps) % board_size

    def pay(self, amount):
        self.money -= amount
        if self.money < 0:
            return False
>>>>>>> 03ef5a75298ff18032c20f31e4eb5562f738139d
        return True