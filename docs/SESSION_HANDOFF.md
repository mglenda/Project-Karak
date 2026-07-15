# Session handoff - Karak refactor

Datum: 2026-07-02

## Kontext projektu

Projekt je Python/pygame implementacia stolovej hry Karak. Autor ho pisal vo volnom case pocas ucenia Pythonu. Najsilnejsia cast projektu je vlastna graficka vrstva nad pygame: UI strom, anchor layout, event dispatch, interaktivna mapa, zoom/pan a bufferovanie textur bez opakovanej degradacie kvality.

## Co sa riesilo v tejto session

1. Vytvorena projektova dokumentacia:
   - `docs/KARAK_PROJECT_DOCUMENTATION.md`
   - Obsahuje architekturu, game loop, herne modely, akcie, buffy, combat, dice, UI vrstvy, assety, zname rizika a workflow pre pridavanie funkcionalit.

2. Analyzovany aktualny dice flow:
   - `GameEngine/Dice.py`
   - `GameEngine/DiceManager.py`
   - `GameEngine/DiceDefinition.py`
   - `UserInterface/DicePanel.py`
   - `GraphicComponents/DiceGraphics.py`
   - `UserInterface/CombatPanel.py`

3. Implementovana animacia hodu kockou:
   - `DiceGraphics` dostal animacny stav.
   - Preblikavanie zacina intervalom 50 ms.
   - Po kazdom prebliknuti sa interval predlzi o 10 ms.
   - Animacia pouziva iba hodnoty validne pre dany typ kocky.
   - Normalna kocka animuje 1-6, Warlock kocka 0-3.

4. Upraveny koniec animacie:
   - Finalna hodnota sa uz nenastavi tvrdo presne v case `duration`.
   - Po poslednom random ticku sa caka este cely posledny interval.
   - Realy cas animacie teda moze mierne presiahnut `duration`, ale rytmus ostava konzistentny.

5. Implementovany pending/commit dice flow:
   - `Dice` ma `pending_value`.
   - `DiceManager` ma `rolling`, `rolling_indices`, `roll_id`.
   - Hod sa najprv vygeneruje ako pending.
   - `DicePanel` animuje pending hodnoty.
   - Az po dokonceni vsetkych animacii sa vola commit.
   - Combat power sa teda vyhodnoti az po animacii.
   - Osetreny edge case: ak padne rovnaka hodnota ako predtym, animacia aj tak prebehne cez `roll_id`.

6. Upraveny `ActionPanel` pocas rolling stavu:
   - pocas hodu sa vycisti a skryje,
   - po hode sa vrati iba ak bol pred hodom viditelny.

## Stav repozitara pred planovanym refactorom

Pouzivatel upratal repo, pridal `.gitignore`, odstranil nechcene subory a pushol zmeny. Pred zacatim architektonickeho refactoru bol `git status --short` cisty.

## Problem so sandboxom

Lokalny Windows sandbox zlyhava pri zapise do existujucich suborov:

```text
windows sandbox failed:
orchestrator_helper_launch_failed:
setup refresh failed to launch helper:
helper=codex-windows-sandbox-setup.exe
error=program not found
```

Dovod: chyba lokalny helper `codex-windows-sandbox-setup.exe` v Codex/CLI tooling.

Docasne riesenie:
- citanie vacsinou funguje,
- pre zapis pouzivat `sandbox_permissions: require_escalated`,
- idealne opravit lokalnu instalaciu Codex CLI / sandbox helper.

## Dohodnuty architektonicky refactor

Ciel: zmensit zavislost na globalnom `GAME` singletone, pretoze nove pravidla zacinaju byt tazko implementovatelne.

Dohodnuty postup po krokoch s pauzou po kazdom kroku:

1. Overit cisty stav a zmapovat zavislosti na `GAME` singleton.
2. Zaviest `GameContext` ako stavovy objekt bez zmeny spravania.
3. Presunut dice flow do `DiceService`.
4. Presunut combat flow do `CombatService`.
5. Presunut movement/tile placement flow do `MovementService`.
6. Presunut reward flow do `RewardService`.
7. Postupne odstranit priame `from Game import GAME` z `GameEngine` a UI vrstiev.
8. Zaverecna syntax/test kontrola a aktualizacia dokumentacie.

## Krok 1 refactoru - hotovy

Zmapovane priame zavislosti na `GAME`:

- `main.py`: hlavny runtime a event loop.
- `GameEngine/Action.py`: combat, reward, turn, dice, movement.
- `GameEngine/TileMap.py`: tile placement, pathfinding, current hero.
- `UserInterface/RewardPanel.py`
- `UserInterface/HeroPanel.py`
- `UserInterface/DicePanel.py`
- `UserInterface/CombatPanel.py`
- `UserInterface/ActionPanel.py`
- `Game.py`: dnes miesa stav, pravidla aj fasadu.

## Krok 2 refactoru - hotovy

Bolo pridane:

- `GameContext.py`

Obsah pridaneho suboru:

```python
from Interfaces.HeroInterface import HeroInterface
from GameEngine.Combat import Combat
from GameEngine.DiceManager import DiceManager
from GameEngine.Reward import Reward
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UI import UI
    from GameEngine.MinionPack import MinionPack
    from Interfaces.TileMapInterface import TileMapInterface


class GameContext:
    def __init__(self) -> None:
        self.ui: "UI" = None
        self.heroes: list[HeroInterface] = []
        self.minion_pack: "MinionPack" = None
        self.combat: Combat = None
        self.dice_manager: DiceManager = None
        self.reward: Reward = None
        self.running: bool = False
        self.rolling_hero: HeroInterface = None
        self.apply_roll_lock: bool = False

    def get_tilemap(self) -> "TileMapInterface":
        return self.ui.get_world().get_tilemap()

    def get_current_hero(self) -> HeroInterface:
        return self.heroes[0]

    def get_current_hero_active(self) -> HeroInterface:
        if self.combat is not None and self.combat.is_arena_duel():
            return self.combat.get_active_duelist()
        return self.get_current_hero()
```

Bolo upravene:

- `Game.py`
- importuje `GameContext`
- `GameContext.ui`, `GameContext.minion_pack` a `GameContext.get_tilemap` su typovane cez `TYPE_CHECKING`, aby IntelliSense videl dostupne metody bez runtime import cyklu
- v `Game.__init__` vytvara `self.context = GameContext()`
- povodne stavove atributy su zachovane ako property proxy do contextu:
  - `ui`
  - `heroes`
  - `minion_pack`
  - `combat`
  - `dice_manager`
  - `running`
  - `reward`
  - `rolling_hero`
  - `apply_roll_lock`
- `get_tilemap`, `get_current_hero` a `get_current_hero_active` deleguju na context

Overenie:

```powershell
python -m py_compile Game.py GameContext.py
```

Prebehlo uspesne.

## Krok 3 refactoru - hotovy

Pouzivatel schvalil pokracovat na krok 3.

Bolo pridane:

- `Services/DiceService.py`

Dice flow bol presunuty z `Game.py` do `DiceService`:

- `create_dice_manager`
- `start_dice_roll`
- `start_dice_reroll`
- `finish_dice_roll`
- `is_dice_rolling`
- `get_dice_manager`
- `clear_dice_manager`

`DiceService` dostava `GameContext` v konstruktore a neimportuje `Game`, aby nevznikol novy cyklus. Zachovane spravanie:

- hod sa ignoruje, ak neexistuje `dice_manager` alebo uz prebieha rolling,
- roll/reroll nastavuje `rolling_hero` a `apply_roll_lock` rovnako ako predtym,
- po spusteni hodu sa vycisti action panel,
- `finish_dice_roll` commituje pending hodnoty,
- ak je zapnuty roll lock, hrdina dostane `CannotRollDices`,
- po dokonceni hodu sa vynuluje `rolling_hero` a `apply_roll_lock`,
- po dokonceni hodu sa vynuti mouse motion refresh.

`Game.py` ostal kompatibilnou fasadou:

- povodne verejne dice metody stale existuju,
- tieto metody iba deleguju do `self.dice_service`,
- UI a `Action.py` sa v tomto kroku nemuseli menit.

Overenie:

```powershell
python -m py_compile Game.py GameContext.py Services/DiceService.py GameEngine/DiceManager.py GameEngine/Dice.py UserInterface/DicePanel.py UserInterface/CombatPanel.py UserInterface/ActionPanel.py GameEngine/Action.py
python -c "import Game"
```

Obe kontroly prebehli uspesne.

## Krok 4 refactoru - hotovy

Pouzivatel schvalil pokracovat na krok 4.

Bolo pridane:

- `Services/CombatService.py`

Combat flow bol presunuty z `Game.py` do `CombatService`:

- `start_combat`
- `end_combat`
- `get_combat`

`CombatService` dostava `GameContext` a `DiceService` v konstruktore. Zachovane spravanie:

- pri starte combat sa vypnu tiles,
- attacker je aktualny hero,
- defender je placeable na aktualnom tile,
- vytvori sa `Combat(attacker, defender)`,
- vytvori sa dice manager pre aktualneho hrdinu,
- pri ukonceni combat sa resetuju combat cooldowny a buffy aktivneho hrdinu,
- draw mimo arena duel vracia aktualneho hrdinu na former tile,
- vyhra miniona explore-ne miniona, zrani hrdinu a vrati ho na former tile,
- prehra miniona odstrani miniona,
- po finalnom combat sa vycisti dice manager, zavola `combat.end()` a combat sa nastavi na `None`,
- pri arena duel pokracovani sa aktivuje dalsi duelist a vytvori sa dice manager pre aktivneho duelista.

`Game.py` ostal kompatibilnou fasadou:

- povodne verejne combat metody stale existuju,
- tieto metody iba deleguju do `self.combat_service`.

Doplnene typovanie pre IntelliSense:

- v `GameContext.py` sa pouziva `TYPE_CHECKING` pre `UI`, `MinionPack` a `TileMapInterface`,
- v `Game.py` sa pouziva `TYPE_CHECKING` pre anotacie `ui: "UI"` a `minion_pack: "MinionPack"`,
- v `Interfaces/TileMapInterface.py` je doplneny stub `disable_all_tiles`, pretoze `GameContext.get_tilemap()` vracia `TileMapInterface` a services tuto metodu volaju,
- pravidlo pre dalsie kroky: ak by priamy import mohol zaviest cyklus alebo sa dnes pouziva iba lokalny import, typovat cez `TYPE_CHECKING` a string anotacie.

Overenie:

```powershell
python -m py_compile Game.py GameContext.py Services/DiceService.py Services/CombatService.py GameEngine/Combat.py GameEngine/Action.py UserInterface/CombatPanel.py
python -c "import Game"
```

Obe kontroly prebehli uspesne.

## Krok 5 refactoru - hotovy

Pouzivatel schvalil pokracovat na krok 5.

Bolo pridane:

- `Services/MovementService.py`

Movement/tile placement flow bol presunuty z `Game.py` do `MovementService`:

- `choose_minion`
- `spawn_minion`
- `confirm_tile_placement`
- `move_to_tile`
- `load_move_options`

`MovementService` dostava `GameContext` v konstruktore. Zachovane spravanie:

- vyber miniona stale taha z `context.minion_pack`,
- pri prazdnom minion packu sa hrdina iba presunie na tile,
- pri jednom vytiahnutom minionovi sa minion spawne a hrdina sa presunie,
- `spawn_minion` stale pouziva lokalny import `Minion`, aby sa nemenila import topologia,
- potvrdenie tile placement odstrani `ChoosingTile`, zaregistruje click na move a riesi spawn tile,
- presun hrdinu resetuje tilemove cooldowny/buffy a znovu nacita move options,
- `load_move_options` zachovalo povodne pravidla pre hostile tile, `IgnoreHostiles`, move points a `CannotMove`.

`Game.py` ostal kompatibilnou fasadou:

- povodne verejne movement metody stale existuju,
- tieto metody iba deleguju do `self.movement_service`,
- existujuce callbacky z `TileMap` cez `GAME.move_to_tile` a `GAME.confirm_tile_placement` ostavaju funkcne.

Upratane importy v `Game.py`:

- odstranene uz nepotrebne movement/combat importy `MinionInterface`, `PlaceableInterface`, `Duelist` a `bMod`.

Overenie:

```powershell
python -m py_compile Game.py GameContext.py Services/DiceService.py Services/CombatService.py Services/MovementService.py GameEngine/TileMap.py GameEngine/Action.py
python -c "import Game"
```

Obe kontroly prebehli uspesne.

## Krok 6 refactoru - hotovy

Pouzivatel schvalil pokracovat na krok 6.

Bolo pridane:

- `Services/RewardService.py`

Reward flow bol presunuty z `Game.py` do `RewardService`:

- `get_reward`
- `create_reward`
- `clear_reward`

`RewardService` dostava `GameContext` v konstruktore. Zachovane spravanie:

- `get_reward` vracia aktualny `context.reward`,
- `clear_reward` nastavi `context.reward = None`,
- `create_reward` zachovalo povodny volaci kontrakt fasady.

Dolezity detail:

- `Game.create_reward(self, item, hero)` ma historicky zavadzajuce nazvy parametrov,
- `Action.py` ju vola pozicne ako `GAME.create_reward(self.hero, self.hero.get_tile().get_placeable())`,
- povodny kod tym vytvoril `Reward(hero, item)` a fungoval spravne,
- tento krok preto nemenil poradie parametrov, aby sa nezmenilo spravanie.

`Game.py` ostal kompatibilnou fasadou:

- povodne verejne reward metody stale existuju,
- tieto metody iba deleguju do `self.reward_service`.

Overenie:

```powershell
python -m py_compile Game.py GameContext.py Services/DiceService.py Services/CombatService.py Services/MovementService.py Services/RewardService.py GameEngine/Reward.py GameEngine/Action.py UserInterface/RewardPanel.py
python -c "import Game"
```

Obe kontroly prebehli uspesne.

## Krok 7 refactoru - hotovy

Pouzivatel schvalil pokracovat na krok 7.

Ciel:

- postupne odstranit priame `from Game import GAME` z `GameEngine` a UI vrstiev,
- zachovat `Game` ako kompatibilnu fasadu,
- nepustat sa este do big bang odstranenia `GAME` z `main.py`.

Odstranene priame `GAME` importy z:

- `UserInterface/HeroPanel.py`
- `UserInterface/ActionPanel.py`
- `UserInterface/DicePanel.py`
- `UserInterface/CombatPanel.py`
- `UserInterface/RewardPanel.py`
- `GameEngine/TileMap.py`
- `GameEngine/Action.py`

Zavedeny explicitny dependency passing:

- `Game.start()` vytvara `UI(self)`,
- `UI` posiela `game` do `World` a vsetkych panelov,
- `World` posiela `game` do `TileMap`,
- `TileMap` pouziva `self.game` pre callbacky a aktualneho hrdinu,
- `Game.spawn_heroes()` vytvara `Hero(..., self)`,
- `Hero` posiela `self.game` do vsetkych `Action` instancii,
- `Action` a potomkovia pouzivaju `self.game` namiesto importovaneho globalu.
- redundantne assignmenty v `Game.__init__` pre stav drzany v `GameContext` boli odstranene,
- `GAME = Game()` ostava na konci `Game.py`, pretoze `main.py` je zatial entrypoint/composition root a stale importuje singleton.

Zachovane spravanie:

- verejne metody `Game` ostali zachovane,
- UI panely stale citaju stav cez rovnakych fasadnych metod,
- dice animation stale vola `finish_dice_roll` po skonceni animacie,
- dice reroll stale vola `start_dice_reroll`,
- action buttony stale volaju `a.run`,
- tile map callbacky stale volaju `move_to_tile` a `confirm_tile_placement`, len cez explicitny `self.game`.

Typovanie:

- pri novych referenciách na `Game` sa pouziva `TYPE_CHECKING` a string anotacie,
- runtime import cykly sa tym nezavadzaju.

Overenie:

```powershell
rg -n "from Game import GAME|\bGAME\." GameEngine UserInterface UI.py GraphicsEngine Interfaces
python -m py_compile Game.py UI.py GraphicsEngine/World.py GameEngine/TileMap.py GameEngine/Action.py GameEngine/Hero.py UserInterface/HeroPanel.py UserInterface/ActionPanel.py UserInterface/DicePanel.py UserInterface/CombatPanel.py UserInterface/RewardPanel.py
python -c "import Game"
python -c "from DataLoader import DataLoader; from Game import GAME; DataLoader.load(); GAME.start(); print(type(GAME.ui).__name__, len(GAME.heroes), type(GAME.get_tilemap()).__name__)"
powershell -NoProfile -Command 'Get-ChildItem -Recurse -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }'
python -c "import Game; print(Game.GAME.is_running(), Game.GAME.get_dice_manager(), Game.GAME.get_reward())"
```

Vysledok:

- `rg` nenasiel ziadne priame `GAME` importy/pouzitia v cielovych vrstvach,
- kompilacia prebehla uspesne,
- `import Game` presiel,
- smoke test vypisal `UI 3 TileMap`,
- sirsia kompilacia vsetkych `.py` suborov prebehla uspesne,
- kontrola pociatocnych context hodnot vypisala `False None None`.

## Krok 8 refactoru - hotovy

Pouzivatel upozornil, ze tenke wrapper metody v `Game`, ktore iba deleguju na `GameContext` alebo services, by nemali zostat dlhodobo.

Ciel:

- odstranit zbytocne read-only wrapper pouzitia,
- nechat command/runtime metody tam, kde maju stale jasny zmysel,
- neprepisovat `main.py`, ktory ostava entrypoint/composition root so singletonom `GAME`.

Prepisane call sites:

- `UserInterface/HeroPanel.py`
  - `self.game.get_current_hero()` -> `self.context.get_current_hero()`
- `UserInterface/ActionPanel.py`
  - dice rolling stav ide cez `self.dice_service`,
  - aktivny hrdina ide cez `self.context.get_current_hero_active()`,
  - `force_mouse_motion` ostava cez `game`, lebo je to runtime/UI command.
- `UserInterface/DicePanel.py`
  - dice manager, finish roll a reroll idu cez `self.dice_service`.
- `UserInterface/CombatPanel.py`
  - combat ide cez `self.combat_service`,
  - dice manager ide cez `self.dice_service`.
- `UserInterface/RewardPanel.py`
  - reward ide cez `self.reward_service`.
- `GameEngine/TileMap.py`
  - aktualny hrdina ide cez `self.context.get_current_hero()`.
- `GameEngine/Action.py`
  - combat commandy idu cez `self.game.combat_service`,
  - reward commandy idu cez `self.game.reward_service`,
  - dice commandy/stav idu cez `self.game.dice_service`,
  - movement refresh ide cez `self.game.movement_service`,
  - `end_turn` ostava cez `game`, lebo turn service este neexistuje.

Odstranene z `Game.py`:

- `get_tilemap`
- `get_current_hero`
- `get_current_hero_active`
- `get_combat`
- `is_dice_rolling`
- `get_dice_manager`
- `get_reward`
- `create_reward`
- `clear_reward`
- `choose_minion`
- `spawn_minion`
- `load_move_options`
- `start_combat`
- `end_combat`
- `create_dice_manager`
- `start_dice_roll`
- `start_dice_reroll`
- `finish_dice_roll`
- `clear_dice_manager`

V `Game.py` ostalo:

- stavove property proxy na `GameContext`,
- runtime lifecycle metody `start`, `quit`, `is_running`,
- setup `spawn_heroes`,
- callbacky pouzivane z `TileMap`: `confirm_tile_placement`, `move_to_tile`,
- turn flow `end_turn` a `refresh_hero`,
- update/draw/UI runtime metody.

Overenie:

```powershell
rg -n "from Game import GAME|\bGAME\." GameEngine UserInterface UI.py GraphicsEngine Interfaces
powershell -NoProfile -Command 'Get-ChildItem -Recurse -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }'
python -c "import Game; print(Game.GAME.is_running(), Game.GAME.dice_service.get_dice_manager(), Game.GAME.reward_service.get_reward())"
python -c "from DataLoader import DataLoader; from Game import GAME; DataLoader.load(); GAME.start(); print(type(GAME.ui).__name__, len(GAME.heroes), GAME.is_running())"
```

Vysledok:

- `rg` nenasiel ziadne priame `GAME` importy/pouzitia v cielovych vrstvach,
- sirsia kompilacia vsetkych `.py` suborov prebehla uspesne,
- pociatocny stav vypisal `False None None`,
- smoke test vypisal `UI 3 True`.

## Krok 9 cleanup - hotovy

Pouzivatel upozornil, ze v `Game.py` stale ostali metody, ktore patria skor do context/service vrstiev:

- `spawn_heroes`
- `end_turn`
- `refresh_hero`
- `move_to_tile`
- `confirm_tile_placement`

Rozhodnutie:

- `GameContext` zostava stavovy objekt, nie miesto pre behavior,
- spawn/setup flow patri do samostatnej setup service,
- turn flow patri do turn service,
- movement callbacky maju ist priamo cez `MovementService`.

Bolo pridane:

- `Services/GameSetupService.py`
- `Services/TurnService.py`

Presunute:

- `spawn_heroes` -> `GameSetupService.spawn_heroes`
  - explicitne zapisuje do `context.heroes`,
  - stale vytvara `Hero(..., game)`, aby action dependency injection ostal funkcny,
  - po setup-e vola `movement_service.load_move_options`.
- `end_turn` -> `TurnService.end_turn`
- `refresh_hero` -> `TurnService.refresh_hero`
- `Action.EndTurn` a `Action.Revitalize` teraz volaju `self.game.turn_service.end_turn()`.

Movement callback cleanup:

- `World` vytvara `TileMap(self, game.context, game.movement_service)`,
- `TileMap` uz nedostava `game`,
- start tile callback vola `movement_service.move_to_tile`,
- tile placement callback vola `movement_service.confirm_tile_placement`,
- `TileMap` cita aktualneho hrdinu cez `context`.

Odstranene z `Game.py`:

- `spawn_heroes`
- `end_turn`
- `refresh_hero`
- `move_to_tile`
- `confirm_tile_placement`

Aktualny obsah `Game.py`:

- service wiring,
- property proxy na `GameContext`,
- lifecycle `start`, `quit`, `is_running`,
- `update`, `update_gui`, `draw`,
- `force_mouse_motion`,
- `GAME = Game()`.

Overenie:

```powershell
powershell -NoProfile -Command 'Get-ChildItem -Recurse -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }'
python -c "from DataLoader import DataLoader; from Game import GAME; DataLoader.load(); GAME.start(); print(type(GAME.ui).__name__, len(GAME.context.heroes), GAME.is_running(), type(GAME.context.get_tilemap()).__name__)"
rg -n "from Game import GAME|\bGAME\." GameEngine UserInterface UI.py GraphicsEngine Interfaces
```

Vysledok:

- sirsia kompilacia vsetkych `.py` suborov prebehla uspesne,
- smoke test vypisal `UI 3 True TileMap`,
- `rg` nenasiel priame `GAME` importy/pouzitia v cielovych vrstvach.

## Krok 10 cleanup - hotovy

Pouzivatel sa spytal, ci property proxy v `Game` su este nutne.

Zistenie:

- po predchadzajucich cleanupoch uz neboli potrebne ako kompatibilna fasada,
- externe pouzitie bolo uz iba `GAME.ui` v `main.py`,
- ostatne pristupy patria priamo na `GameContext`.

Zmeny:

- odstranene vsetky property proxy z `Game.py`:
  - `ui`
  - `heroes`
  - `minion_pack`
  - `combat`
  - `dice_manager`
  - `running`
  - `reward`
  - `rolling_hero`
  - `apply_roll_lock`
- `Game` teraz cita/zapisuje stav explicitne cez `self.context.*`,
- `main.py` pre pygame eventy pouziva `GAME.context.ui`,
- `Game.py` uz neimportuje typy, ktore boli potrebne len pre proxy anotacie.

Aktualny obsah `Game.py`:

- `__init__` vytvara `GameContext` a services,
- `start` nastavi `context.running`, vytvori `context.ui`, `context.minion_pack` a spusti setup service,
- `quit`, `is_running`,
- `update`, `update_gui`, `draw`,
- `force_mouse_motion`,
- `GAME = Game()`.

Overenie:

```powershell
rg -n "GAME\.(ui|heroes|minion_pack|combat|dice_manager|running|reward|rolling_hero|apply_roll_lock)|self\.(ui|heroes|minion_pack|combat|dice_manager|running|reward|rolling_hero|apply_roll_lock)\b|@property" Game.py main.py GameEngine UserInterface UI.py GraphicsEngine
python -m py_compile Game.py main.py GameContext.py
python -c "from DataLoader import DataLoader; from Game import GAME; DataLoader.load(); GAME.start(); print(type(GAME.context.ui).__name__, len(GAME.context.heroes), GAME.is_running())"
powershell -NoProfile -Command 'Get-ChildItem -Recurse -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }'
```

Vysledok:

- proxy ani `GAME.ui` uz nie su v `Game`/`main.py`,
- smoke test vypisal `UI 3 True`,
- sirsia kompilacia vsetkych `.py` suborov prebehla uspesne.

## Plan pre dalsie pokracovanie

Najblizsi dalsi krok:

1. Skontrolovat `git status --short`.
2. Po schvaleni pouzivatelom pokracovat na zaverecnu kontrolu:
   - spustit sirsiu syntax kontrolu projektu,
   - prebehnut zostavajuce `GAME` pouzitia mimo cielovych vrstiev,
   - aktualizovat dokumentaciu podla finalneho stavu refactoru.
3. Potom zastavit a dat pouzivatelovi finalny suhrn celeho refactoru.

Zastavit sa a dat pouzivatelovi suhrn zaverecnej kontroly.

## Dolezite rozhodnutia

- Nerobit big bang rewrite.
- `Game` zatial ponechat ako fasadu.
- Graficky engine nemenit, iba ho pripadne neskor napojit na explicitny context.
- Pri typoch bez vhodneho priameho runtime importu pouzivat `TYPE_CHECKING` a string anotacie, aby IntelliSense fungoval bez import cyklov.
- `.pyc` a `__pycache__` boli upratane cez `.gitignore`, dalej ich netreba riesit.
- Preklepy typu `enter_comat`, `destory_unknowns`, `agressive` riesit iba ak budu priamo v dotknutom flow.

