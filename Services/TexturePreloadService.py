from core.MemoryEngine import MEMORY_ENGINE
from GameContext import GameContext
from GameEngine.Constants import Constants
from GraphicsEngine.World import ZOOM_MAX, ZOOM_MIN
import inspect
from typing import Callable


class TexturePreloadService:
    def __init__(self, context: GameContext) -> None:
        self.context = context
        self.texture_specs = None

    def preload(self, progress_callback: Callable[[int, int, str], None] = None) -> None:
        ui = self.context.ui
        if ui is None:
            return

        screen = ui.screen
        screen_h = screen.get_h()

        self.texture_specs = []
        self.preload_tiles()
        self.preload_tile_placeables()
        self.preload_hero_panels(screen_h)
        self.preload_inventory(screen_h)
        self.preload_actions(screen_h)
        self.preload_dice(screen_h)
        self.preload_combat(screen_h)
        self.preload_reward(screen_h)
        specs = list(dict.fromkeys(self.texture_specs))
        self.texture_specs = None

        total = len(specs)
        if progress_callback is not None:
            progress_callback(0, total, "Preparing textures")

        for index, (path, w, h, angle, alpha) in enumerate(specs, start=1):
            MEMORY_ENGINE.get_img_buffer().get(path=path, w=w, h=h, angle=angle, alpha=alpha)
            if progress_callback is not None:
                progress_callback(index, total, path)

    def preload_image(self, path: str, w: int, h: int, angle: int = 0, alpha: int = 255) -> None:
        if path is None:
            return
        if self.texture_specs is not None:
            self.texture_specs.append((path, round(w, 4), round(h, 4), angle, alpha))
            return
        MEMORY_ENGINE.get_img_buffer().get(path=path, w=w, h=h, angle=angle, alpha=alpha)

    def preload_square(self, path: str, size: int, angle: int = 0, alpha: int = 255) -> None:
        self.preload_image(path, size, size, angle, alpha)

    def get_tile_sizes(self) -> list[int]:
        default_size = Constants.DEFAULT_TILESIZE
        return [default_size + zoom * 10 for zoom in range(ZOOM_MIN, ZOOM_MAX + 1)]

    def get_definition_paths(self, module, attr_name: str = "path") -> list[str]:
        paths = []
        for _, value in inspect.getmembers(module, inspect.isclass):
            path = getattr(value, attr_name, None)
            if path is not None and path not in paths:
                paths.append(path)
        return paths

    def preload_tiles(self) -> None:
        import GameEngine.TileDefinitions as tile_definitions

        angles = [0, 90, 180, 270]
        for path in self.get_definition_paths(tile_definitions):
            for size in self.get_tile_sizes():
                for angle in angles:
                    self.preload_square(path, size, angle)

    def preload_tile_placeables(self) -> None:
        import GameEngine.HeroDefinition as hero_definitions
        import GameEngine.MinionDefinition as minion_definitions
        import GameEngine.ItemDefinition as item_definitions

        minion_paths = self.get_definition_paths(minion_definitions)
        item_paths = self.get_definition_paths(item_definitions)
        hero_icon_paths = self.get_definition_paths(hero_definitions, "icon_path")
        wheel_path = '_Textures\\Minions\\PowerWheel.png'

        for tile_size in self.get_tile_sizes():
            placeable_size = tile_size * 0.6
            wheel_size = placeable_size * 0.55
            for path in minion_paths + item_paths:
                self.preload_square(path, placeable_size)
            self.preload_square(wheel_path, wheel_size)

            for hero_count in range(1, 6):
                for has_placeable in (False, True):
                    visible_count = hero_count if not has_placeable else 5
                    icon_size = (0.7 - 0.065 * visible_count) * tile_size
                    for path in hero_icon_paths:
                        self.preload_square(path, icon_size)

    def preload_hero_panels(self, screen_h: int) -> None:
        import GameEngine.HeroDefinition as hero_definitions

        panel_h = screen_h * 0.35
        portrait_w = panel_h * 0.72 * 0.8
        portrait_h = panel_h * 0.8
        for path in self.get_definition_paths(hero_definitions, "portrait_path"):
            self.preload_image(path, portrait_w, portrait_h)

        icon_size = portrait_h * 0.1
        self.preload_square('_Textures\\HeroPanel\\MovePoints.png', icon_size)
        self.preload_square('_Textures\\HeroPanel\\HitPoints_Green.png', icon_size)

    def preload_inventory(self, screen_h: int) -> None:
        import GameEngine.ItemDefinition as item_definitions

        panel_h = screen_h * 0.35
        portrait_w = panel_h * 0.72 * 0.8
        inventory_slot_size = portrait_w * 0.2
        theme_size = inventory_slot_size * 0.6
        item_size = inventory_slot_size * 0.9

        for path in (
            '_Textures\\Inventory\\ScrollSlot.png',
            '_Textures\\Inventory\\KeySlot.png',
            '_Textures\\Inventory\\WeaponSlot.png',
        ):
            self.preload_square(path, theme_size)

        for path in self.get_definition_paths(item_definitions):
            self.preload_square(path, item_size)

    def preload_actions(self, screen_h: int) -> None:
        import GameEngine.Action as actions

        button_size = screen_h * 0.125 * 0.95
        focus_size = button_size * 0.95
        for _, value in inspect.getmembers(actions, inspect.isclass):
            for attr_name in ("path", "path_focused"):
                path = getattr(value, attr_name, None)
                if path is not None:
                    self.preload_square(path, button_size)
        self.preload_square('_Textures\\Abilities\\FocusLayer.png', focus_size)

    def preload_dice(self, screen_h: int) -> None:
        dice_size = screen_h * 0.25 * 0.5
        paths = ['_Textures\\Dice\\None.png', '_Textures\\Dice\\FocusLayer.png']
        paths.extend([
            '_Textures\\Dice\\Zero.png',
            '_Textures\\Dice\\One.png',
            '_Textures\\Dice\\Two.png',
            '_Textures\\Dice\\Three.png',
            '_Textures\\Dice\\Four.png',
            '_Textures\\Dice\\Five.png',
            '_Textures\\Dice\\Six.png',
        ])
        for path in paths:
            self.preload_square(path, dice_size)

    def preload_combat(self, screen_h: int) -> None:
        import GameEngine.HeroDefinition as hero_definitions
        import GameEngine.MinionDefinition as minion_definitions

        combat_h = screen_h
        duelist_w = combat_h * 0.34
        duelist_h = combat_h * 0.24
        portrait_size = duelist_h
        indicator_h = duelist_h * 0.1
        total_circle_size = duelist_h * 0.4

        for path in self.get_definition_paths(hero_definitions, "combat_icon_path"):
            self.preload_square(path, portrait_size)
        for path in self.get_definition_paths(minion_definitions):
            self.preload_square(path, portrait_size)

        for path in (
            '_Textures\\Combat\\Modifier_Dice.png',
            '_Textures\\Combat\\Modifier_Base.png',
            '_Textures\\Combat\\Modifier_Ability.png',
            '_Textures\\Combat\\Modifier_Scroll.png',
        ):
            self.preload_square(path, indicator_h)
        self.preload_square('_Textures\\Combat\\Total_Circle.png', total_circle_size)

    def preload_reward(self, screen_h: int) -> None:
        import GameEngine.ItemDefinition as item_definitions

        item_size = screen_h * 0.15
        for path in self.get_definition_paths(item_definitions):
            self.preload_square(path, item_size)
        self.preload_square('_Textures\\Heroes\\Combat\\BeastHunter.png', item_size)
