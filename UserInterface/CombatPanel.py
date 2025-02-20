from GraphicComponents.CombatScreen import CombatScreen,Frame,FRAMEPOINT

from Game import GAME

class CombatPanel():
    main: CombatScreen

    def __init__(self,screen: Frame) -> None:
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
        if GAME.get_combat() is not None:
            if not self.is_visible():
                self.show()
            
            if GAME.get_dice_manager().get_value() != GAME.get_combat().get_active_duelist_data().get_dice_power():
                GAME.get_combat().get_active_duelist_data().set_dice_power(GAME.get_dice_manager().get_value())

            for id in range(2):
                self.main.update(id=id
                                ,base_value = GAME.get_combat().get_duelist_data(id).get_power()
                                ,dice_value = GAME.get_combat().get_duelist_data(id).get_dice_power()
                                ,ability_value = GAME.get_combat().get_duelist_data(id).get_ability_power()
                                ,scroll_value = GAME.get_combat().get_duelist_data(id).get_scroll_power()
                                ,total_value = GAME.get_combat().get_duelist_data(id).get_total_power()
                                ,portrait = GAME.get_combat().get_duelist_data(id).duelist.get_combat_icon_path()
                )
        else:
            if self.is_visible():
                self.hide()