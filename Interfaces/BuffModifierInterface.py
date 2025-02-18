from Interfaces.Interface import Interface

class BuffModifierInterface(Interface):
    hero: Interface
    
    def apply(self):
        pass

    def remove(self):
        pass