# Verification guide

## Baseline checks

Check the worktree before and after edits:

```powershell
git status --short
git diff --check
git diff -- <changed paths>
```

Compile changed integration surfaces:

```powershell
python -m py_compile Game.py GameContext.py <changed files and direct callers>
```

For cross-layer changes, compile the whole source tree without treating generated caches as deliverables:

```powershell
Get-ChildItem -Recurse -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }
```

Run at least an import smoke test:

```powershell
python -c "import Game"
```

Use a short construction/state-transition script only when it will not enter the pygame loop. Set a dummy SDL video driver if display initialization requires it. Do not mutate persistent external state.

## Targeted searches

Search for forbidden or stale wiring:

```powershell
rg -n "from Game import GAME|\bGAME\." GameEngine Services UserInterface GraphicComponents GraphicsEngine UI.py
rg -n "OldName|old_method" .
```

Search asset references and confirm every new file/path exists. Search every new class or service name to confirm definition, construction, registration, call sites, and cleanup.

## Behavioral matrix

For each feature, check:

- entry preconditions and action availability;
- behavior while active, including conflicting input;
- successful and alternate outcomes;
- combat, tile-move, turn, or manual cleanup;
- UI visibility and dynamic child destruction;
- action/movement refresh and stationary-pointer refresh;
- inventory capacity/replacement where relevant;
- dice pending versus committed values where relevant;
- current hero versus active arena duelist where relevant.

## Reporting

Distinguish clearly among:

- static inspection;
- syntax compilation;
- import/construction smoke tests;
- automated behavioral tests;
- interactive pygame validation.

If interactive behavior was not run, name the exact scenario the user should verify manually.
