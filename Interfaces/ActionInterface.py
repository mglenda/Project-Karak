from Interfaces.Interface import Interface

class ActionInterface(Interface):
    hero: Interface
    path: str
    path_focused: str
    prio: int

    def is_available(self) -> bool:
        pass

    def run(self):
        pass