class Cooldown:
    scope: int

    def __init__(self, duration_scope: int):
        self.scope = duration_scope

    def get_scope(self) -> int:
        return self.scope
    
