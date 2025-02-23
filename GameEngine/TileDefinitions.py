PATH = '_Textures\\Tiles\\Retextured\\'

class TileDefinition():
    pathing: list = ()
    path: str
    is_spawn: bool
    is_arena: bool
    is_portal: bool
    is_healing: bool
    is_cursed: bool

class Unknown(TileDefinition):
    pathing: tuple = (1,1,1,1)
    path: str = PATH + 'Background.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class Start(TileDefinition):
    pathing: tuple = (1,1,1,1)
    path: str = PATH + 'Start.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = True
    is_cursed = False

class CorridorCorner(TileDefinition):
    pathing: tuple = (0,1,1,0)
    path: str = PATH + 'CorridorCorner.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class Arena(TileDefinition):
    pathing: tuple = (1,0,1,0)
    path: str = PATH + 'Arena.png'
    is_spawn = False
    is_arena = True
    is_portal = False
    is_healing = False
    is_cursed = False

class Chamber(TileDefinition):
    pathing: tuple = (1,0,1,0)
    path: str = PATH + 'Chamber.png'
    is_spawn = True
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class ChamberCorner(TileDefinition):
    pathing: tuple = (0,1,1,0)
    path: str = PATH + 'ChamberCorner.png'
    is_spawn = True
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class ChamberCross(TileDefinition):
    pathing: tuple = (1,1,1,1)
    path: str = PATH + 'ChamberCross.png'
    is_spawn = True
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class ChamberT(TileDefinition):
    pathing: tuple = (0,1,1,1)
    path: str = PATH + 'ChamberT.png'
    is_spawn = True
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class Corridor(TileDefinition):
    pathing: tuple = (1,0,1,0)
    path: str = PATH + 'Corridor.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class CorridorCross(TileDefinition):
    pathing: tuple = (1,1,1,1)
    path: str = PATH + 'CorridorCross.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class CorridorT(TileDefinition):
    pathing: tuple = (1,0,1,1)
    path: str = PATH + 'CorridorT.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = False

class Curse(TileDefinition):
    pathing: tuple = (1,1,1,1)
    path: str = PATH + 'Curse.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = False
    is_cursed = True

class Fountain(TileDefinition):
    pathing: tuple = (0,1,1,0)
    path: str = PATH + 'Fountain.png'
    is_spawn = False
    is_arena = False
    is_portal = False
    is_healing = True
    is_cursed = False

class Portal(TileDefinition):
    pathing: tuple = (1,0,1,0)
    path: str = PATH + 'Portal.png'
    is_spawn = False
    is_arena = False
    is_portal = True
    is_healing = False
    is_cursed = False