from GraphicsEngine.Tile import Tile,Frame,Image,FRAMEPOINT
from GraphicsEngine.Placeable import Placeable as GPlaceable
from GraphicsEngine.Constants import MouseEvent
from GameEngine.TileDefinitions import TileDefinition
from Interfaces.TileObjectInterface import TileObjectInterface
from Interfaces.HeroInterface import HeroInterface
from Interfaces.PlaceableInterface import PlaceableInterface

class TileObject(TileObjectInterface):
    g_tile: Tile
    pathing: tuple
    path: str
    definition: TileDefinition
    is_spawn: bool
    column: int
    row: int
    
    heroes: list[HeroInterface]
    hero_icons: list[Image]
    placeable: PlaceableInterface
    g_placeable: GPlaceable

    def __init__(self, definition: TileDefinition, size: int, world: Frame,row: int, column: int) -> None:
        self.pathing = definition.pathing
        self.path = definition.path
        self.is_spawn = definition.is_spawn
        self.definition = definition

        self.row = row
        self.column = column

        self.g_tile = Tile(size,definition.path,world)
        self.heroes: list[HeroInterface] = []
        self.hero_icons: list[Image] = []
        self.placeable = None
        self.g_placeable = None

    def add_placeable(self, placeable: PlaceableInterface):
        self.placeable = placeable
        self.graphics_refresh_placeable()
        self.graphics_refresh_heroes()

    def remove_placeable(self):
        self.placeable = None
        self.graphics_refresh_placeable()
        self.graphics_refresh_heroes()

    def get_placeable(self) -> PlaceableInterface:
        return self.placeable
    
    def graphics_refresh_placeable(self):
        if self.placeable is None:
            self.g_placeable.destroy()
            self.g_placeable = None
        else:
            if self.g_placeable is None:
                self.g_placeable = GPlaceable(self.g_tile.get_w()*0.6,self.g_tile.get_h()*0.6,self.placeable.get_path(),self.g_tile)
                self.g_placeable.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
            else:
                self.g_placeable.set_texture(self.placeable.get_path())

            value = self.placeable.get_wheel_value()
            if value is None:
                self.g_placeable.hide_wheel()
            else:
                self.g_placeable.show_wheel()
                self.g_placeable.set_wheel_value(value)
            

    def add_hero(self, hero: HeroInterface):
        if hero not in self.heroes:
            self.heroes.append(hero)
            self.graphics_refresh_heroes()

    def remove_hero(self, hero: HeroInterface):
        if hero in self.heroes:
            self.heroes.remove(hero)
            self.graphics_refresh_heroes()

    def graphics_refresh_heroes(self):
        for i in reversed(self.hero_icons):
            i.destroy()
            self.hero_icons.remove(i)

        icon_size = self.graphics_get_hero_icon_size()
        for i,h in enumerate(self.heroes):
            icon = Image(icon_size,icon_size,h.get_icon_path(),self.g_tile)

            if i == 0:
                if len(self.heroes) == 1 and self.placeable is None:
                    icon.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
                else:
                    icon.set_point(FRAMEPOINT.TOPRIGHT,FRAMEPOINT.TOPRIGHT)
            elif i == 1:
                if len(self.heroes) == 2:
                    icon.set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMLEFT)
                else:
                    icon.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)
            elif i == 2:
                if len(self.heroes) == 3:
                    icon.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM)
                else:
                    icon.set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMLEFT)
            elif i == 3:
                icon.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT)
            elif i == 4:
                icon.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

            self.hero_icons.append(icon)

    def graphics_get_hero_icon_size(self) -> int:
        return (0.7 - 0.065 * (len(self.heroes) if self.placeable is None else 5)) * self.g_tile.get_h()

    def set_type(self, definition: TileDefinition):
        self.pathing = definition.pathing
        self.path = definition.path
        self.is_spawn = definition.is_spawn
        self.definition = definition
        self.g_tile.set_texture(self.path)

    def get_definition(self) -> TileDefinition:
        return self.definition
    
    def set_active(self, active: bool):
        self.g_tile.set_active(active)

    def on_click(self,func,*args):
        self.g_tile.register_mouse_event(MouseEvent.LEFTCLICK,func,*args)

    def rotate_off(self):
        self.g_tile.clear_mouse_event(MouseEvent.WHEELUP)
        self.g_tile.clear_mouse_event(MouseEvent.WHEELDOWN)

    def clear_mouse_events(self):
        self.g_tile.clear_all_events()
    
    def rotate_up(self):
        self.pathing = (
            self.pathing[1]
            ,self.pathing[2]
            ,self.pathing[3]
            ,self.pathing[0]
        )
        self.g_tile.rotate(90)
    
    def rotate_down(self):
        self.pathing = (
            self.pathing[3]
            ,self.pathing[0]
            ,self.pathing[1]
            ,self.pathing[2]
        )
        self.g_tile.rotate(-90)

    def destroy(self):
        self.g_tile.destroy()