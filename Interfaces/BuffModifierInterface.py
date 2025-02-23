from Interfaces.Interface import Interface

class BuffModifierInterface(Interface):
    hero: Interface
    
    def enable(self):
        pass

    def disable(self):
        pass

    def remove(self):
        pass