import GameEngine.MinionDefinition as Minions
import random

class MinionPack():
    pack: list[Minions.MinionDefinition]
    def __init__(self):
        self.pack = []
        for _ in range(8):
            self.pack.append(Minions.Rat)
        for _ in range(1):
            self.pack.append(Minions.Dragon)
        for _ in range(2):
            self.pack.append(Minions.Fiend)
        for _ in range(2):
            self.pack.append(Minions.SkeletonMage)
        for _ in range(3):
            self.pack.append(Minions.SkeletonKing)
        for _ in range(4):
            self.pack.append(Minions.GiantSpider)
        for _ in range(8):
            self.pack.append(Minions.Mummy)
        for _ in range(6):
            self.pack.append(Minions.GiantBat)
        for _ in range(5):
            self.pack.append(Minions.SkeletonWarrior)
        for _ in range(12):
            self.pack.append(Minions.SkeletonKeymaster)
        for _ in range(10):
            self.pack.append(Minions.ChestClosed)
        random.shuffle(self.pack)

    def pick(self, count: int = 1) -> list[Minions.MinionDefinition]:
        arr: list[Minions.MinionDefinition] = []
        for _ in range(count):
            if len(self.pack) > 0:
                arr.append(self.pack.pop())
        return arr
    
    def put(self, arr: list[Minions.MinionDefinition]):
        if len(arr) > 0:
            for m in arr:
                self.pack.append(m)
            random.shuffle(self.pack)
    
    def get_count(self) -> int:
        return len(self.pack)