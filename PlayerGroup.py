from Player import Player

class PlayerGroup():
    Players = []

    def __init__(self) -> None:
        pass

    def add(self,player:Player):
        self.Players.append(player)

    def remove(self,player:Player):
        self.Players.remove(player)

    def get_all(self):
        return self.Players