class Duelist():
    power: int

    def get_combat_icon_path(self) -> str:
        pass

    def get_weapon_power(self) -> int:
        return self.power
    
    def is_in_combat(self) -> bool:
        return self.in_combat if hasattr(self, 'in_combat') else False
    
    def enter_comat(self):
        self.in_combat = True

    def leave_combat(self):
        self.in_combat = False