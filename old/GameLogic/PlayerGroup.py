from GameLogic.Player import Player

MAXIMUM_PLAYERS = 5

class PlayerGroup():
    _Players = []
    _current: int

    def __init__(self) -> None:
        self._current = -1

    def add(self,player:Player):
        self._Players.append(player)

    def remove(self,player:Player):
        self._Players.remove(player)

    def get_all(self):
        return self._Players
    
    def get(self,i:int) -> Player:
        return self._Players[i]
    
    def get_count(self):
        return len(self._Players)
    