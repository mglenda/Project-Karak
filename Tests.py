import Ability
import Hero
import Inventory
import Items
import Player
import PlayerGroup
import Minion


p = Player.Player('Marek')
p.set_hero(Hero.Wizard())

print(p.get_name())
print(p.get_hero().get_abilities())
p.get_hero().add_item(Items.Key())
key = p.get_hero().get_item(Items.Key)
p.get_hero().remove_item(key)
print(p.get_hero().get_item(Items.Key))
print(p.get_hero().has_ability(Ability.UnlockChest))