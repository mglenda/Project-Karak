---
name: karak-feature-development
description: Extend and modify the Karak Python/pygame project while preserving its current architecture, dependency flow, gameplay conventions, UI framework, and asset patterns. Use when implementing new gameplay functionality, actions or hero abilities, buffs and modifiers, services and multi-step flows, items, minions, tiles, inventory or rewards, UI panels, graphic components, or changes spanning GameEngine, Services, UserInterface, GraphicComponents, GraphicsEngine, GameContext, Game, and project assets.
---

# Develop Karak Features

## Start from the live repository

1. Read `references/architecture.md` and `references/conventions.md` before designing a change.
2. Read `references/feature-playbooks.md` for the requested feature category.
3. Inspect every current call site and neighboring implementation involved in the requested flow. Treat repository code as authoritative; treat `docs/` and `ToDoList.txt` as historical or planning context that may be stale.
4. Check `git status --short` and preserve unrelated or user-owned changes.
5. Search with `rg` before introducing a new abstraction, API, asset path, constant, or duplicated behavior.

## Design the smallest coherent change

- Put persistent shared runtime state in `GameContext` only when multiple collaborators need it.
- Put orchestration and multi-object game flows in a focused service under `Services/`.
- Put entity-owned state and invariants on the relevant `GameEngine` model.
- Put declarative catalog data in the corresponding `*Definition.py` or `*Pack.py` module.
- Let `UserInterface` panels observe state, rebuild or update visuals, and register callbacks; keep game rules out of panels.
- Put reusable composed visuals in `GraphicComponents`; change `GraphicsEngine` only for generic rendering, layout, input, or caching capability.
- Wire new top-level dependencies in `Game.__init__`, pass them explicitly, and avoid new imports of the global `GAME` outside the entrypoint.
- Preserve compatibility only when a current caller needs it. Do not add forwarding wrappers to `Game` merely for convenience.

Before editing, trace the complete lifecycle: trigger, availability, state mutation, UI refresh, input blocking, cleanup/reset, and next-turn or next-phase behavior. For asynchronous dice or timed UI flows, also trace pending state, callback completion, and cancellation/cleanup.

## Implement in dependency order

Work from the domain outward:

1. Add or adjust constants, definitions, model state, modifiers, buffs, and actions.
2. Add or extend the owning service and context state.
3. Wire dependencies at the composition root.
4. Add graphic components and state-sync panels.
5. Register the panel in `UI` and its update in `Game.update_gui()` when periodic synchronization is required.
6. Add assets using the existing directory and Windows-style relative path conventions.
7. Refresh affected action availability, movement options, mouse hover state, or cached surfaces explicitly where the existing flow requires it.

Follow local naming and formatting even when imperfect. Do not opportunistically fix established misspellings such as `agressive` or `destory_unknowns` unless the requested flow requires a coordinated rename.

## Verify behavior

Use `references/verification.md` to choose checks proportional to the change. At minimum:

1. Compile every changed Python file and its direct integration files.
2. Compile the full Python tree for cross-module changes.
3. Run a headless or non-looping smoke test when construction and state transitions can be exercised safely.
4. Search for stale callers, forbidden global `GAME` dependencies, missing wiring, and wrong asset paths.
5. Manually reason through availability and cleanup boundaries for combat, tile movement, turn, forever buffs, dice animation, modal panels, and inventory replacement.

Do not claim runtime gameplay validation if only compilation or import checks ran. Report validation scope and any unverified pygame interaction explicitly.

