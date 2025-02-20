class DiceDefinition:
    values: list[int]

class Normal(DiceDefinition):
    values: list[int] = [1,2,3,4,5,6]

class Warlock(DiceDefinition):
    values: list[int] = [0,1,2,3]