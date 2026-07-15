# Feature playbooks

## Hero ability or action

1. Identify trigger, common availability restrictions, priority, action types, cooldown boundary, passive visibility, and cleanup.
2. Add a modifier for a queryable/reversible rule and a buff for duration-bound state.
3. Add the action in `GameEngine/Action.py`, following the closest existing action.
4. Delegate multi-phase behavior to the relevant service; add a focused service only when no owner exists.
5. Register hero-specific actions in `HeroDefinition.special_actions`; mark universal actions `is_default = True`.
6. Add ability icons and validate both paths.
7. Exercise unavailable, available, running, completion, and reset states.

## Service-backed multi-step flow

1. Model explicit phases and terminal cleanup before coding.
2. Keep service-owned ephemeral state on the service; put state in `GameContext` only when UI or another service must consume it directly.
3. Inject dependencies in `Game.__init__` and pass them through constructors.
4. Expose narrow commands/queries; avoid a generic manager or new `Game` forwarding facade.
5. Disable conflicting tile/action input while active.
6. On completion, clear dice/timers/callbacks/modal state, refresh actions and movement, and refresh stationary mouse hover.

## Item, inventory, or reward

1. Add an `ItemDefinition` with `type`, `power`, score metadata if relevant, and texture.
2. Verify slot compatibility, capacity, replacement/leftover semantics, consumption, and tile ownership.
3. Add an action for active use or pickup when needed.
4. Route multi-object pickup/trading through `RewardService` or a focused successor.
5. Update ranking or combat-derived queries through model methods, not UI calculations.
6. Test free slot, full inventory, compatible replacement, incompatible slot, leftover on tile, and consumable depletion.

## Minion

1. Add a `MinionDefinition` with power, `agressive`, reward definition, and texture.
2. Add its count to `MinionPack` and preserve pick/put randomization.
3. Verify explored state, combat result, removal, reward placement, and non-aggressive behavior where relevant.

## Tile or movement rule

1. Add a definition and texture; preserve pathing order top/right/bottom/left.
2. Add the tile count to `TilePack`.
3. Extend `MovementService` for movement-side effects and `TileMap` for selection/path visualization.
4. Preserve unknown-tile placement, rotation accessibility, portal handling, wall-passing rules, and hostile blocking.
5. Verify normal entry, special entry, interruption/modal flow, cleanup, and restored move options.

## UI panel

1. Decide whether a reusable graphic component is needed.
2. Build the frame tree with proportional sizes and anchors.
3. Create a game-aware panel that reads context/service state and tracks loaded values.
4. Instantiate it in `UI`, add a getter if existing code uses getters, and update it from `Game.update_gui()` if polling is required.
5. Add modal blocking in `UI.draw()` when appropriate.
6. Register input events, destroy dynamic children safely, and refresh mouse state after interaction topology changes.
7. Verify hidden, shown, updated, dismissed, and overlapping-input states.

## Generic graphics capability

Modify `GraphicsEngine` only if the feature is reusable beyond one gameplay panel. Preserve recursive frame ownership, attachment propagation, cache refresh behavior, reverse-order mouse dispatch, visibility, and active-state semantics. Validate at least two consumers or keep the behavior in a higher-level component.

