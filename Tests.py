import GameLogic.Ability as Ability
import GameLogic.Hero as Hero
import GameLogic.Inventory as Inventory
import GameLogic.Items as Items
import GameLogic.Player as Player
import GameLogic.PlayerGroup as PlayerGroup
import GameLogic.Minion as Minion


p = Player.Player('Marek')
p.set_hero(Hero.Wizard())

print(p.get_name())
print(p.get_hero().get_abilities())
p.get_hero().add_item(Items.Key())
key = p.get_hero().get_item(Items.Key)
p.get_hero().remove_item(key)
print(p.get_hero().get_item(Items.Key))
print(p.get_hero().has_ability(Ability.UnlockChest))

b = Hero.Barbarian()
b2 = Hero.Barbarian()
w = Hero.Wizard()

b.remove_ability(Ability.Perseverance)

x:int = 12
f:float = 12.5

print(x < f)