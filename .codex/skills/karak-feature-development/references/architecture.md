# Current architecture

## Dependency direction

`main.py` is the executable entrypoint and owns the global `GAME`. `Game.py` is the composition root and lifecycle coordinator. It constructs `GameContext` and all services, creates `UI`, initializes packs, calls setup, runs service/model updates, and dispatches GUI updates.

Prefer this direction:

`main / Game` -> `Services + UI` -> `GameEngine models + GraphicComponents` -> `GraphicsEngine + core`

Avoid reverse dependencies. Use `TYPE_CHECKING` and quoted annotations where runtime imports would create cycles. Import locally only when that matches an existing cycle-breaking boundary.

## Responsibilities

### `GameContext.py`

Hold shared runtime references and state: UI, heroes, active combat, dice manager, reward, rolling metadata, and stable cross-feature state. Provide state-derived queries such as current hero or ranking. Do not turn the context into a general behavior/service object.

### `Services/`

Coordinate workflows involving multiple models or phases. Existing examples:

- `DiceService`: pending roll, animation completion callback, commit, roll lock, cleanup.
- `CombatService`: combat lifecycle and dice integration.
- `MovementService`: tile placement, movement, curse prompt/timer, movement availability.
- `RewardService`: pickup, slot replacement, reward completion.
- `TurnService`: turn rotation and duration reset.
- `GameSetupService`: initial heroes and placement.
- `TexturePreloadService`: deterministic asset-cache warming.

Inject `GameContext` and only the collaborating services needed. Register a new service in `Game.__init__`. Prefer direct service use at call sites over thin `Game` facade methods.

### `GameEngine/`

Hold domain entities and rules:

- Models: `Hero`, `Duelist`, `Combat`, `Inventory`, `Item`, `Minion`, `TileObject`, dice and reward objects.
- Definitions: class-level data in `HeroDefinition`, `ItemDefinition`, `MinionDefinition`, `TileDefinitions`, and `DiceDefinition`.
- Catalogs: `TilePack` and `MinionPack` own counts, randomization, pick/put behavior.
- Extensible mechanics: `Action`, `Buff`, and `BuffModifier` subclasses.

Definition classes are passed as types, not instantiated. Preserve comparisons and annotations accordingly.

### UI layers

- `UserInterface/`: panels that read context/services/models, synchronize visible state in `update()`, and register user callbacks.
- `GraphicComponents/`: reusable composed visuals without gameplay decisions.
- `GraphicsEngine/`: generic pygame tree, anchors, surfaces, mouse dispatch, world interaction, and caching.
- `core/`: surface buffers and callback wrapper.

Create visuals as children of `Frame`. Position them with `set_point(child_anchor, parent_anchor, offsets, optional_anchor_parent)`. Visibility does not itself guarantee input; mouse registration activates elements. Modal visibility must also participate in `UI.draw()` blocking through `DisableScreen` when appropriate.

## Runtime lifecycle

- `main.py` runs logic and GUI update threads and processes pygame input/drawing.
- `Game.update()` currently updates timed movement flow and action availability.
- `Game.update_gui()` explicitly updates each panel; wire new polling panels here.
- `UI.draw()` controls modal blocking, then draws the screen tree.
- `MouseController` dispatches to the topmost active colliding element in reverse tree order.
- `MEMORY_ENGINE` caches images, text, fitted text, and rect surfaces. Use setters or `refresh_surface()` after visual property changes.

## Important boundaries

- Do not import `GAME` into `GameEngine`, services, UI, or graphics. Pass `Game`, context, services, or narrow callbacks explicitly.
- Keep game-state mutations out of graphic components.
- Keep reusable rendering behavior out of gameplay services.
- Do not add shared context state for temporary data owned by a single service unless another collaborator genuinely consumes it.
- Account for unsynchronized logic and GUI threads: keep transitions short and avoid partially initialized observable state.

