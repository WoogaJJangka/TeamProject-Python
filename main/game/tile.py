<<<<<<< HEAD
class Tile:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.owner = None
        self.price = 1000
        self.toll = int(self.price * 1.3)
        self.upgrade_level = 0

    def upgrade(self):
        if self.upgrade_level == 0:
            self.upgrade_level = 1
            self.toll = int((self.price + 500) * 1.8)
        elif self.upgrade_level == 1:
            self.upgrade_level = 2
            self.toll = int((self.price + 500 + 1000) * 2.2)

    def get_total_value(self):
        # 총 투자 금액 반환
        if self.upgrade_level == 0:
            return self.price
        elif self.upgrade_level == 1:
            return self.price + 500
        else:
=======
class Tile:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.owner = None
        self.price = 1000
        self.toll = int(self.price * 1.3)
        self.upgrade_level = 0

    def upgrade(self):
        if self.upgrade_level == 0:
            self.upgrade_level = 1
            self.toll = int((self.price + 500) * 1.8)
        elif self.upgrade_level == 1:
            self.upgrade_level = 2
            self.toll = int((self.price + 500 + 1000) * 2.2)

    def get_total_value(self):
        # 총 투자 금액 반환
        if self.upgrade_level == 0:
            return self.price
        elif self.upgrade_level == 1:
            return self.price + 500
        else:
>>>>>>> 03ef5a75298ff18032c20f31e4eb5562f738139d
            return self.price + 500 + 1000