import pygame

class KeyboardBehavior():
    def on_key_hold(self, keys: pygame.key.ScancodeWrapper, unicode: str):
        pass
    
    def on_key_pressed(self, key: int, unicode: str):
        pass
   
    def on_key_released(self, key: int, unicode: str):
        pass
    

class FocusedElement():
    focused: KeyboardBehavior = None

    def set(self,element: KeyboardBehavior):
        if element is None or isinstance(element,KeyboardBehavior):
            self.focused = element 

    def get(self) -> KeyboardBehavior:
        return self.focused
    
FOCUSED = FocusedElement()