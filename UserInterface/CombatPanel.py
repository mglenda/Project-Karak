from GraphicComponents.CombatScreen import CombatScreen,Frame,FRAMEPOINT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class CombatPanel():
    main: CombatScreen

    def __init__(self,screen: Frame, game: "Game") -> None:
        self.combat_service = game.combat_service
        self.dice_service = game.dice_service
        self.main = CombatScreen(screen.get_h(),screen.get_h(),screen)
        self.main.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.main.set_visible(False)

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self)-> bool:
        return self.main.is_visible()

    def update(self):
        combat = self.combat_service.get_combat()
        if combat is not None:
            if not self.is_visible():
                self.show()
            
            combat.get_active_duelist().set_dice_power(self.dice_service.get_dice_manager().get_value())

            for id in range(2):
                self.main.update(id=id
                                ,base_value = combat.get_duelist(id).get_weapon_power()
                                ,dice_value = combat.get_duelist(id).get_dice_power()
                                ,ability_value = combat.get_duelist(id).get_ability_power()
                                ,scroll_value = combat.get_duelist(id).get_scroll_power()
                                ,total_value = combat.get_duelist(id).get_total_power()
                                ,portrait = combat.get_duelist(id).get_combat_icon_path()
                )
        else:
            if self.is_visible():
                self.hide()
