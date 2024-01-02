import GUI.Tiles as Tiles
import random

class TilePack():
    def __init__(self):
        self.pack = []
        for i in range(4):
            self.pack.append(Tiles.CorridorCorner)
        for i in range(6):
            self.pack.append(Tiles.Arena)
        for i in range(4):
            self.pack.append(Tiles.Portal)
        for i in range(2):
            self.pack.append(Tiles.Fountain)
        for i in range(5):
            self.pack.append(Tiles.CorridorT)
        for i in range(7):
            self.pack.append(Tiles.CorridorCross)
        for i in range(16):
            self.pack.append(Tiles.ChamberCross)
        for i in range(17):
            self.pack.append(Tiles.ChamberT)
        for i in range(15):
            self.pack.append(Tiles.ChamberCorner)
        for i in range(13):
            self.pack.append(Tiles.Chamber)
        for i in range(4):
            self.pack.append(Tiles.Curse)
        random.shuffle(self.pack)

    def pick(self):
        if len(self.pack) > 0:
            return self.pack.pop()
        return None