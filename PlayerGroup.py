from Player import Player

class PlayerGroup():
    _Players = []

    def __init__(self) -> None:
        pass

    def add(self,player:Player):
        self._Players.append(player)

    def remove(self,player:Player):
        self._Players.remove(player)

    def get_all(self):
        return self._Players
    
    def get(self,i:int):
        return self._Players[i]
