# Project conventions and invariants

## Python and imports

- Use PascalCase modules and classes where the project already does so; use snake_case methods and variables.
- Use explicit type hints in touched code without undertaking unrelated modernization.
- Add `from __future__ import annotations` when it simplifies cross-references consistently with neighboring files.
- Put type-only imports under `TYPE_CHECKING`; use quoted annotations to avoid runtime cycles.
- Prefer module aliases `import GameEngine.Buff as buff`, `import GameEngine.BuffModifier as bMod`, and definition aliases when neighboring code uses them.
- Preserve relative Windows asset paths such as `_Textures\\Abilities\\Name.png`.

## Actions

An `Action` subclass normally declares class attributes: `path`, `path_focused`, `prio`, `action_types`, `modifiers_default`, `passive`, and when relevant `default_scope`, `is_default`, or `available_during_curse_roll`.

- Call `super().get_availability()` unless the action intentionally bypasses common restrictions.
- Put context-sensitive ordering in `update_priority()`; `Hero.refresh_actions()` calls `update()` and available actions are sorted by priority.
- Put state mutation in `run()` and delegate multi-object flow to a service.
- Call `super().run()` when the default cooldown applies.
- Set `is_default = True` for actions every hero should discover through `get_default_action_types()`.
- Add hero-specific actions to `HeroDefinition.special_actions`.
- Passive actions remain hidden from `ActionPanel` but can expose modifiers while available.
- Refresh actions after state changes that affect availability. Recompute movement options or force mouse motion when the interactive surface changes.

The base availability blocks most actions during curse rolling, blocks actions under `CannotDoAnything`, blocks abilities while cursed, and blocks non-combat actions while injured. Preserve or explicitly justify exceptions.

## Buffs, modifiers, and durations

Use a modifier as a queryable rule flag or reversible numeric contribution. Use a buff as a timed container of modifier instances.

Duration scopes reset by numeric threshold:

- combat: `0`
- tile move: `1`
- turn: `5`
- forever/manual: `1000`

`remove_buffs(scope)` removes buffs whose scope is less than or equal to the reset scope. Choose scope by cleanup boundary, and verify both modifier enable and disable behavior. Numeric modifiers must be reversible and must not double-enable through repeated refreshes.

## Shared flow and dice

Use services for state machines spanning entities or UI. For dice-dependent flows:

1. Create a manager with definition types.
2. Start a pending roll through `DiceService`.
3. Let `DicePanel` animate pending values.
4. Commit only in `finish_dice_roll()`.
5. Use `on_finish` for feature-specific resolution.
6. Clear manager and feature state at the owning flow's terminal boundary.

Do not resolve gameplay from pending dice values or bypass the animation/commit protocol.

## UI and graphic components

- Pass `game` to panels that require services/context, then store the narrow collaborators used.
- Initialize stable visual children once; rebuild dynamic children only when source identity/count changes.
- Use cached `current_*` or `loaded_*` values to avoid unnecessary texture/text reconstruction.
- Destroy dynamic frames before clearing Python lists.
- Use `show()`, `hide()`, and `is_visible()` for modal panels.
- Register mouse callbacks with `register_mouse_event`; remember registration makes an element active.
- Call `game.force_mouse_motion()` or the established service equivalent after changing buttons under a stationary cursor.
- Add modal panels to `UI.draw()`'s disable-screen condition.
- Split a feature into `GraphicComponents/<Visual>.py` and `UserInterface/<Panel>.py` when it has a reusable composed visual and a game-aware synchronizer.

## Definitions, packs, and assets

- Add class-level fields to the correct definition base and every concrete definition when the field has no safe default.
- Add new catalog entries/counts to the corresponding pack.
- Keep tile `pathing` order top, right, bottom, left.
- Place assets in the established folders: abilities, heroes, minions, items, tiles, numbers, or panel-specific directories.
- Search every referenced asset path and confirm the file exists. Focused and normal icons may intentionally share a path when no focused variant exists.

## Existing quirks

Treat these as compatibility constraints unless directly in scope:

- Definition classes are used as values.
- Several established identifiers are misspelled (`agressive`, `destory_unknowns`).
- Some older code uses broad imports or redundant constructors.
- `Action.py` is large; avoid unrelated splitting during a feature change.
- `TileObject.graphics_refresh_placeable()` assumes an existing graphic when removing a placeable; be careful when introducing new removal paths.
- There is no established automated test suite or package configuration in the repository.

