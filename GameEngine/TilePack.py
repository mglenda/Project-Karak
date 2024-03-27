import GameEngine.TileDefinitions as Tiles
import random

class TilePack():
    pack: list[Tiles.TileDefinition]
    def __init__(self):
        self.pack = []
        for _ in range(4):
            self.pack.append(Tiles.CorridorCorner)
        for _ in range(6):
            self.pack.append(Tiles.Arena)
        for _ in range(4):
            self.pack.append(Tiles.Portal)
        for _ in range(2):
            self.pack.append(Tiles.Fountain)
        for _ in range(5):
            self.pack.append(Tiles.CorridorT)
        for _ in range(7):
            self.pack.append(Tiles.CorridorCross)
        for _ in range(16):
            self.pack.append(Tiles.ChamberCross)
        for _ in range(17):
            self.pack.append(Tiles.ChamberT)
        for _ in range(15):
            self.pack.append(Tiles.ChamberCorner)
        for _ in range(13):
            self.pack.append(Tiles.Chamber)
        for _ in range(4):
            self.pack.append(Tiles.Curse)
        random.shuffle(self.pack)

    def pick(self) -> Tiles.TileDefinition:
        if len(self.pack) > 0:
            return self.pack.pop()
        return None
    
    def get_count(self) -> int:
        return len(self.pack)