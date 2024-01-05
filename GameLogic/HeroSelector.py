import GameLogic.Hero as Hero
import random

class HeroSelector():
    pack: list = []
    i: int
    def __init__(self) -> None:
        self.pack.append(Hero.Acrobat)
        self.pack.append(Hero.Barbarian)
        self.pack.append(Hero.BattleMage)
        self.pack.append(Hero.Oracle)
        self.pack.append(Hero.Ranger)
        self.pack.append(Hero.Swordsman)
        self.pack.append(Hero.Thief)
        self.pack.append(Hero.Warlock)
        self.pack.append(Hero.Warrior)
        self.pack.append(Hero.Wizard)
        self.i = len(self.pack)-1
    
    def get_next(self) -> Hero.Hero:
        self.i += 1
        if self.i >= len(self.pack):
            self.i = 0
        return self.pack[self.i]
    
    def get_previos(self) -> Hero.Hero:
        self.i -= 1
        if self.i < 0:
            self.i = len(self.pack) - 1
        return self.pack[self.i]
    
    def get_random(self) -> Hero.Hero:
        self.i = random.randint(0,len(self.pack)-1)
        return self.pack[self.i]
