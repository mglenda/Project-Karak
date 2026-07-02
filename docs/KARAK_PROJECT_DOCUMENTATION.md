# Karak Python/Pygame - projektova dokumentacia

Tento dokument zachytava aktualnu strukturu projektu Karak a prakticke pravidla pre buducu implementaciu funkcionalit. Projekt je digitalna implementacia stolovej hry Karak v Pythone s vlastnou pygame grafickou vrstvou, hernym jadrom a UI panelmi.

## Rychly prehlad

Vstupny bod aplikacie je `main.py`. Globalny stav hry drzi singleton `GAME` v `Game.py`. Herna logika je primarne v `GameEngine/`, vykreslovacia a event vrstva v `GraphicsEngine/`, skladane vizualne komponenty v `GraphicComponents/` a panely napojene na `GAME` v `UserInterface/`.

Najdolezitejsia zasada: nove pravidla hry a data patria do `GameEngine`; `UserInterface` a `GraphicComponents` maju iba zobrazovat aktualny stav a registrovat pouzivatelske akcie.

## Spustenie a hlavny cyklus

`main.py`:

- inicializuje pygame a fonty,
- vola `DataLoader.load()`,
- spusti `GAME.start()`,
- spusti dva daemon thready:
  - `AppLogic.update()` vola `GAME.update()` na 60 FPS,
  - `Graphics.update()` vola `GAME.update_gui()` na 60 FPS,
- hlavny thread spracovava pygame eventy, deleguje ich na `GAME.ui` a vola `GAME.draw()` na 120 FPS.

`DataLoader.py` momentalne pridava defaultne akcie hrdinom:

- `Thief`: `Stealth`, `Backstab`,
- `Wizard`: `AstralWalking`.

Pozor: `DataLoader.load_hero_defaults()` robi `append` do class-level listov. Ak by sa `load()` volalo viackrat v jednom procese, defaultne akcie sa zdubluju.

## Globalny stav hry

`Game.py` definuje triedu `Game` a singleton `GAME = Game()`.

`Game.start()`:

- nastavi `running = True`,
- vytvori `UI`,
- vytvori `MinionPack`,
- zavola `spawn_heroes()`.

`Game` drzi hlavne runtime objekty:

- `ui`: instancia `UI`,
- `heroes`: list aktualnych hrdinov v poradi tahu,
- `minion_pack`: balicek priser,
- `combat`: aktivny `Combat` alebo `None`,
- `dice_manager`: aktivny `DiceManager` alebo `None`,
- `reward`: aktivny `Reward` alebo `None`.

Aktualny hrdina je vzdy `heroes[0]`. `end_turn()` rotuje zoznam hrdinov tak, ze aktualny hrdina ide na koniec, potom refreshne noveho aktualneho hrdinu a nacita jeho moznosti pohybu.

`get_current_hero_active()` vracia:

- aktivneho duelanta pocas hero-vs-hero arena duelu,
- inak bezneho aktualneho hrdinu.

## Herny model

### Hrdina

`GameEngine/Hero.py`

`Hero` dedi z `HeroInterface`, ktory dedi z `Duelist`. Hrdina obsahuje:

- `definition`: trieda z `HeroDefinition.py`,
- `name`,
- `tile` a `former_tile`,
- `hit_points`, `max_hit_points`,
- `move_points`, `max_move_points`,
- `inventory`,
- `actions`,
- `active_buffs`,
- `power`.

Zakladne akcie pridane kazdemu hrdinovi:

- `EndTurn`,
- `ActionCombat`,
- `RollDice`,
- `Revitalize`,
- `HealingFountain`,
- `PickUpItem`.

Potom sa pridaju akcie z `definition.default_actions` a zoznam sa sortuje podla `prio`.

Dolezite metody:

- `move_to_tile(tile)`: presunie hrdinu, aktualizuje tile zoznamy hrdinov a znizi move point o 1, ak bol kladny.
- `move_to_former_tile()`: vrati hrdinu na predosle pole.
- `get_available_actions()`: vrati dostupne akcie podla cooldownov, buffov a modifierov.
- `add_buff(buff_type, duration_scope=None)`: vytvori buff instanciu.
- `remove_buffs(scope_or_type)`: odstrani buffy podla duration scope alebo typu.
- `has_modifier(mod_type)`: hlada modifier v aktivnych buffoch aj dostupnych akciach.

### HeroDefinition

`GameEngine/HeroDefinition.py`

Definicie hrdinov su class-level data:

- `portrait_path`,
- `icon_path`,
- `combat_icon_path`,
- `default_actions`.

Aktualne su definovani hrdinovia: `Wizard`, `Warrior`, `Warlock`, `Thief`, `Swordsman`, `Ranger`, `Oracle`, `LordOfKarak`, `BattleMage`, `Barbarian`, `Acrobat`, `WarriorPrincess`, `BeastHunter`, `Alchemist`.

Pri pridani noveho hrdinu treba:

- pridat triedu do `HeroDefinition.py`,
- doplnit assety do `_Textures/Heroes/...`,
- pridat defaultne akcie cez `DataLoader.load_hero_defaults()` alebo priamo do definicie,
- podla potreby ho spawnovat v `Game.spawn_heroes()`.

### Akcie

`GameEngine/Action.py`

`Action` je zakladna trieda pre aktivne aj pasivne schopnosti. Dolezite atributy:

- `path`, `path_focused`: ikony v UI,
- `prio`: poradie v action paneli,
- `default_scope`: cooldown scope po `run()`,
- `action_types`: general/combat/ability/scroll,
- `modifiers_default`: buff modifier triedy, ktore akcia poskytuje,
- `passive`: ci sa ma skryt z action panelu.

`Action.get_availability()` standardne kontroluje:

- cooldown je `None`,
- hrdina nema `CannotDoAnything`,
- ability nie je dostupna pri `Cursed`,
- non-combat akcia nie je dostupna pri `Injured`.

Existujuce akcie:

- `ActionCombat`: start/end combat.
- `PickUpItem`: zobrazi/skryje reward panel pre item na tile.
- `EndTurn`: ukonci tah.
- `Stealth`: pasivny flag `IgnoreHostiles`, implementacia `run()` je zatial vypnuta.
- `RollDice`: hodi aktivne kocky a prida buff `CannotRollDices`.
- `Revitalize`: odstrani `Injured`, vylieci 1 HP a ukonci tah.
- `HealingFountain`: lieci na fontane alebo odstrani curse.
- `AstralWalking`: pasivny `CanWalkThroughWalls`.
- `Ambush`: pasivny `AbilityPower_Plus_1`, len proti explored minionovi.
- `Backstab`: pasivny `WinOnDraw`.

Pri novej akcii:

1. Vytvor triedu v `Action.py` alebo samostatnom module, ak narastie pocet schopnosti.
2. Nastav `path`, `path_focused`, `prio`, `action_types`, `modifiers_default`, `passive`.
3. Prepis `get_availability()`.
4. Implementuj `run()`.
5. Pridaj akciu do hrdinu cez `DataLoader` alebo `HeroDefinition.default_actions`.
6. Ak akcia potrebuje UI specialny stav, napoj ho cez `Game` a existujuce panely.

### Buff a modifier system

`GameEngine/Buff.py`, `GameEngine/BuffModifier.py`

Buff je kontajner modifierov s duration scope. Modifier je vacsinou marker/flag, ktory sa zistuje cez `hero.has_modifier(...)`.

Duration scopes v `GameEngine/Constants.py`:

- `DURATION_SCOPE_COMBAT = 0`,
- `DURATION_SCOPE_TILEMOVE = 1`,
- `DURATION_SCOPE_TURN = 5`,
- `DURATION_SCOPE_FOREVER = 1000`.

Odstranovanie buffov funguje pravidlom `buff.scope <= reset_scope`. Napriklad pri pohybe sa resetuju tilemove buffy, pri konci tahu turn buffy.

Existujuce buffy:

- `Stealth`: `IgnoreHostiles`,
- `Exhausted`: `CannotStartCombat`,
- `ChoosingTile`: `CannotEndTurn`, `CannotDoAnything`,
- `CannotRollDices`: `CannotRollDice`,
- `Unconsciousness`: `CannotStartCombat`, `Injured`, `CannotMove`,
- `Injured`: `CannotStartCombat`, `Injured`, `CannotEndTurn`, `CannotMove`,
- `Curse`: `Cursed`,
- `HealedOnFountain`: `CannotStartCombat`, `Injured`, `CannotMove`,
- `DisableAllActions`: `CannotEndTurn`, `CannotDoAnything`, `CannotMove`.

Modifier `AbilityPower_Plus_1` je specialny: pri enable zvysi ability power o 1 a pri disable znizi o 1.

### Suboj

`GameEngine/Combat.py`, `GameEngine/Duelist.py`

`Combat` obsahuje dvoch duelantov a aktivneho duelanta. Pri vytvoreni zavola `enter_comat()` na oboch objektoch. Metoda ma preklep v nazve, ale pouziva sa konzistentne.

Power v suboji:

`total = weapon_power + ability_power + dice_power + scroll_power`

`CombatPanel.update()` priebezne nastavuje aktivnemu duelantovi `dice_power` z `DiceManager.get_value()`.

Vyhodnotenie:

- remiza je remiza, ak maju rovnaky total a bud obaja maju `WinOnDraw`, alebo ho nema nikto,
- ak presne jeden ma `WinOnDraw`, vyhrava pri rovnosti,
- pri minion combate `is_finished()` vracia true hned po aktivnom hrdinovi,
- pri arena hero-vs-hero sa prepne aktivny duelant na druheho hrdinu.

`Game.end_combat()`:

- pri remize mimo areny vrati hrdinu na `former_tile`,
- ak vyhra minion, minion sa oznaci explored, hrdina strati HP a vrati sa,
- ak prehra minion, odstrani sa a na tile sa polozi reward item,
- combat vycisti dice manager a stav combat.

### Kocky

`GameEngine/DiceDefinition.py`, `Dice.py`, `DiceManager.py`

Definicie:

- `Normal`: hodnoty `[1,2,3,4,5,6]`,
- `Warlock`: hodnoty `[0,1,2,3]`.

`Hero.get_dices()` aktualne vracia `[Normal, Normal, Warlock]` pre kazdeho hrdinu.

`DiceManager.roll()` hodi vsetky kocky. `get_value()` vracia sucet aktualnych hodnot, `None` sa pocita ako 0.

### Inventar a itemy

`GameEngine/Inventory.py`, `InventorySlot.py`, `Item.py`, `ItemDefinition.py`

Sloty:

- `MAX_WEAPONS = 2`,
- `MAX_SCROLLS = 3`,
- `MAX_KEYS = 1`.

Chest itemy sa nedavaju do slotov, ale do `Inventory.chests`.

`ItemDefinition.py` obsahuje:

- zbrane: `Dagger` power 1, `Sword` power 2, `Axe` power 3,
- key: `Key`,
- chest: `Chest`, `DragonChest`,
- scrolls: `MagicBolt`, `ThornOfDarkness`, `HealingPortal`, `FrostFist`.

`Inventory.add_item(item, slot=None)`:

- chest vlozi do `chests`,
- bez slotu vlozi prvy kompatibilny volny slot,
- so slotom nahradi obsah slotu a vrati leftover.

### Placeable, Minion, Reward

`Placeable` je objekt umiestnitelny na tile. `set_tile(tile)` odoberie objekt zo stareho tile a prida ho na novy.

`Minion` dedi z `MinionInterface` a `Placeable`. Drzi:

- `power`,
- `agressive`,
- `explored`.

`Minion.remove()` odstrani miniona a prida na jeho tile item podla `definition.reward`.

`Reward` obsahuje `hero` a `item`; pouziva ho `RewardPanel`.

## Mapa, dlazdice a pohyb

`GameEngine/TileDefinitions.py`

`pathing` je tuple v poradi:

1. top,
2. right,
3. bottom,
4. left.

Hodnota `1` znamena priechod, `0` stenu. Rotacia v `TileObject.rotate_up/down()` rotuje aj `pathing`.

`TileMap`:

- zacina jednym `Start` tile v strede sveta,
- okolo priechodov spawnuje `Unknown` tile,
- klik na `Unknown` vytiahne novu tile definiciu z `TilePack`,
- pocas vyberu tile prida hrdinovi buff `ChoosingTile`,
- wheel up/down rotuje tile do validneho pripojenia,
- po potvrdeni sa spawnuju dalsie unknown tile a `Game.confirm_tile_placement()` riesi presun/spawn miniona.

Pohyb:

- `Game.load_move_options()` aktivuje dostupne polia cez `TileMap.load_path(tile, 1)`,
- aktualne sa vzdy pocita iba dosah 1 krok; viac move pointov znamena viac opakovanych krokov,
- ak hrdina stoji na agresivnom minionovi a nema `IgnoreHostiles`, mapa sa deaktivuje,
- `CanWalkThroughWalls` umoznuje pathfinding cez steny na existujuce ne-unknown tiles.

`TilePack.py` obsahuje pevne pocty tile typov a pri inicializacii ich zamiesa.

## Minion pack

`GameEngine/MinionPack.py`

Balicek obsahuje class-level definicie minionov v tychto poctoch:

- `Rat`: 8,
- `Dragon`: 1,
- `Fiend`: 2,
- `SkeletonMage`: 2,
- `SkeletonKing`: 3,
- `GiantSpider`: 4,
- `Mummy`: 8,
- `GiantBat`: 6,
- `SkeletonWarrior`: 5,
- `SkeletonKeymaster`: 12,
- `ChestClosed`: 10.

`pick(count=1)` vracia list definicii. `put(arr)` vrati definicie do balicka a zamiesa ho.

## Graficky engine

`GraphicsEngine/`

Projekt ma vlastny UI framework nad pygame:

- `Element`: pozicia, rozmery, viditelnost, alpha, rotacia.
- `MouseBehavior`: registracia a vykonanie mouse eventov.
- `Frame`: stromova struktura, parent/children, attach pointy, resize, destroy.
- `Image`: frame s texturou z `MemoryEngine`.
- `Rect`: frame s plnou farbou.
- `TextField` a `NumberImage`: text/bitmap cisla.
- `Screen`: fullscreen pygame surface a draw loop.
- `World`: herny svet, drag mapy a zoom.
- `Tile`: graficka tile s active/focus overlaymi.

Anchor body su v `GraphicsEngine/Constants.py`:

- `TOP`, `TOPLEFT`, `TOPRIGHT`,
- `CENTER`,
- `LEFT`, `RIGHT`,
- `BOTTOM`, `BOTTOMLEFT`, `BOTTOMRIGHT`.

`Frame.set_point(att_point, att_point_parent, x_offset=0, y_offset=0, parent=None)` pripevni element k parentovi alebo inemu frame. Pri zmene pozicie parenta sa attachnute deti prepoctu.

### Mouse dispatch

`MouseController` prechadza `screen.get_abs_children()` v reverznom poradi. Event dostane prvy aktivny a kolidujuci element. Preto:

- element musi byt `active`, aby prijimal eventy,
- `register_mouse_event()` automaticky nastavi `active=True`,
- viditelnost sama nestaci,
- prekryvne panely musia byt v strome vyssie alebo musia deaktivovat spodne interakcie.

### Cache textur

`core/MemoryEngine.py`, `core/Buffer.py`

`MEMORY_ENGINE` cacheuje:

- obrazky podla path, sirky, vysky, uhla a alpha,
- text podla textu, fontu, farby, velkosti, uhla a alpha,
- rect povrchy podla farby, rozmerov a alpha.

Pri zmene path/velkosti/rotacie/alpha treba zavolat `refresh_surface()` alebo pouzit existujuce setter metody, ktore ho volaju.

## UI vrstvy

`UI.py` vytvara:

- `World`,
- `HeroPanel`,
- `DisableScreen`,
- `CombatPanel`,
- `DicePanel`,
- `RewardPanel`,
- `ActionPanel`.

`UI.draw()` zobrazi `DisableScreen`, ak je aktivny combat panel alebo reward panel, potom vykresli `screen`.

### UserInterface panely

`UserInterface/ActionPanel.py`

- cita `GAME.get_current_hero_active().get_available_actions()`,
- pri zmene zoznamu znici a znovu vytvori action buttony,
- pasivne akcie sa nezobrazuju,
- klik na button vola `a.run()`.

`UserInterface/DicePanel.py`

- zobrazi sa, ak existuje `GAME.get_dice_manager()`,
- vytvara `DiceGraphics` pre aktualne kocky,
- priebezne nastavuje zobrazene hodnoty,
- vie aktivovat kocky pre reroll cez `activate_dices()`.

`UserInterface/CombatPanel.py`

- zobrazi sa pri aktivnom `GAME.get_combat()`,
- aktualizuje silu oboch duelantov a combat portrety.

`UserInterface/HeroPanel.py`

- zobrazuje portret aktualneho hrdinu, HP, move points a inventory panel.

`UserInterface/InventoryPanel.py`

- renderuje sloty z `hero.inventory.slots`,
- pri zmene slot objektov panel reloadne.

`UserInterface/RewardPanel.py`

- zobrazi sa pri aktivnom `GAME.get_reward()`,
- vykresluje item a jeho power.

## Assety

Hlavne priecinky:

- `_Textures/Abilities/`: ikony akcii,
- `_Textures/Heroes/Retextured/`: portrety,
- `_Textures/Heroes/MyIcons/`: ikony hrdinov na mape,
- `_Textures/Heroes/Combat/`: combat portrety,
- `_Textures/Tiles/Retextured/`: tile textury,
- `_Textures/Minions/Retextured/`: minioni,
- `_Textures/Items/Retextured/`: itemy,
- `_Textures/Numbers/<Color>/`: bitmap cisla,
- `_Fonts/`: fonty,
- `_Rules/`: PDF pravidla.

Projekt pouziva relativne Windows-style path stringy s backslashmi.

## Aktualne rozpracovane funkcionality

`ToDoList.txt` popisuje plan pre looting/reward system a viacero ability:

- reward panel pre vyhru nad minionom,
- loot panel pri vyhre nad hrdinom,
- dvihanie itemov a truhiel,
- `Tactical Reposition`,
- `Dual Wielding`,
- `Stoneskin`,
- `Transformation`,
- combat scroll efekty,
- teleport/heal akcie ako `Protector`.

V kode uz existuje cast reward systemu:

- `GameEngine/Reward.py`,
- `Interfaces/RewardInterface.py`,
- `GraphicComponents/RewardScreen.py`,
- `UserInterface/RewardPanel.py`,
- `PickUpItem` akcia.

## Zname rizika a technicky dlh

Tieto body su pozorovania zo zdrojoveho kodu, nie navrh okamzitej zmeny:

- V repozitari su trackovane alebo pritomne `__pycache__` a `.pyc` subory. Pri buducej hygiene projektu by mali ist do `.gitignore`.
- `GameEngine/Loot.py` a `Interfaces/LootInterface.py` su v git stave zmazane, ale pycache stale existuje.
- `Game.create_reward(item, hero)` ma signaturu `item, hero`, ale `Reward.__init__` ocakava `hero, item` a `PickUpItem.run()` vola `GAME.create_reward(self.hero, item)`. Treba zosuladit pred dalsim loot systemom.
- `TileObject.graphics_refresh_placeable()` pri `placeable is None` vola `self.g_placeable.destroy()` bez kontroly `None`.
- `Minion.remove()` pouziva `super(Placeable,self).remove()`, co je neobvykle a treba overit, ci skutocne vola zamyslany remove chain.
- `Combat.__init__()` vola `enter_comat()` s preklepom; metoda existuje v `Duelist`, preto to funguje, ale nazov je rizikovy.
- `TileMap.destory_unknowns()` ma preklep v nazve.
- `Frame.destroy()` vola `self.parent.remove(self)` bez kontroly `parent is not None`. Root screen by sa nemal destroyovat.
- `DataLoader.load_hero_defaults()` moze duplikovat akcie pri opakovanom volani.
- `AppLogic` a `Graphics` thread pristupuju ku `GAME` bez synchronizacie. Pri pygame UI to moze sposobit race conditions, ak zacnu byt operacie zlozitejsie.
- Typove anotacie casto pouzivaju triedy definicii ako hodnoty, napriklad `Hero(Wizard, 'Marek')`, cize v projekte sa casto pracuje s triedami namiesto instancii definicii.

## Odporucany workflow pri pridavani funkcionalit

### Nova ability hrdinu

1. Pridaj alebo uprav `BuffModifier`, ak ability meni pravidla globalne.
2. Pridaj `Buff`, ak efekt potrebuje trvanie.
3. Pridaj `Action` triedu s dostupnostou a `run()`.
4. Dopln ikony do `_Textures/Abilities/`.
5. Napoj ability na hrdinu cez `DataLoader`.
6. Over `ActionPanel`, combat a reset scope.

### Novy item

1. Pridaj definiciu do `ItemDefinition.py`.
2. Dopln texturu do `_Textures/Items/Retextured/`.
3. Ak ma byt reward, nastav ho na minionovi v `MinionDefinition.py`.
4. Ak ma aktivny efekt, pridaj `Action` alebo logiku v inventory/loot systeme.

### Novy minion

1. Pridaj definiciu do `MinionDefinition.py`.
2. Dopln texturu do `_Textures/Minions/Retextured/`.
3. Nastav `power`, `agressive`, `reward`.
4. Pridaj pocet do `MinionPack.py`.

### Nova tile

1. Pridaj definiciu do `TileDefinitions.py`.
2. Nastav `pathing` v poradi top/right/bottom/left.
3. Nastav flagy `is_spawn`, `is_arena`, `is_portal`, `is_healing`, `is_cursed`.
4. Dopln texturu do `_Textures/Tiles/Retextured/`.
5. Pridaj pocet do `TilePack.py`.
6. Ak tile potrebuje specialne pravidlo, napoj ho v `Game.move_to_tile()`, `confirm_tile_placement()` alebo cez novu akciu/buff.

### Novy UI panel

1. Vytvor vizualny komponent v `GraphicComponents/`.
2. Vytvor state-sync panel v `UserInterface/`.
3. Pridaj instanciu do `UI.__init__()`.
4. Pridaj update volanie do `Game.update_gui()`.
5. Ak panel blokuje mapu, uprav `UI.draw()` a `DisableScreen`.
6. Eventy registruj cez `register_mouse_event()`.

## Mentalny model projektu

Projekt je zatial najviac podobny prototypu s centralnym singletonom. Najrychlejsia cesta pre nove pravidla je:

- stav ulozit na `Game`, `Hero`, `TileObject`, `Inventory`, `Combat` alebo `Reward`,
- pravidlo implementovat v `GameEngine`,
- UI nechat citat stav a volat akcie,
- graficke komponenty udrzat bez znalosti pravidiel hry.

Pri vacsich zmenach bude vhodne najprv stabilizovat reward/loot flow a potom rozdelit `Action.py` na viac suborov, pretoze schopnosti budu hlavnym miestom rastu projektu.
