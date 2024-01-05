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

print(1325 % 360)

l = [1,2,3,4,5,6,7,8,9,10,11,12]

for i in reversed(l):
    l.remove(i)

print(l)