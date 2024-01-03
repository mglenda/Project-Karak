from Hero import Hero

class Player():
    _name:str = 'Player'
    _hero:Hero = None

    def __init__(self,name):
        self._name = name

    def get_name(self):
        return self._name
    
    def set_hero(self,hero:Hero):
        self._hero = hero

    def get_hero(self):
        return self._hero