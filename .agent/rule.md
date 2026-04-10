# BellyUp Project — AI Assistant Rules

## Core Rule: Documentation-First Responses

All answers about AnyLogic must be **grounded in the official AnyLogic documentation** at [anylogic.help](https://anylogic.help). Before giving advice, read or cite the relevant doc page.

---

## AnyLogic Documentation Reference URLs

| Topic | URL |
|---|---|
| Pedestrian Library overview | https://anylogic.help/library-reference-guides/pedestrian-library/index.html |
| Pedestrian space markup | https://anylogic.help/markup/pedestrian-markup.html |
| Rectangular Node | https://anylogic.help/markup/node-r-ped.html |
| Polygonal Node | https://anylogic.help/markup/node-p-ped.html |
| Wall | https://anylogic.help/markup/wall.html |
| Rectangular Wall | https://anylogic.help/markup/rectangular-wall.html |
| Circular Wall | https://anylogic.help/markup/circular-wall.html |
| Attractor | https://anylogic.help/markup/attractor-ped.html |
| Target Line | https://anylogic.help/markup/targetline.html |
| PedSource | https://anylogic.help/library-reference-guides/pedestrian-library/pedsource.html |
| PedSink | https://anylogic.help/library-reference-guides/pedestrian-library/pedsink.html |
| PedGoTo | https://anylogic.help/library-reference-guides/pedestrian-library/pedgoto.html |
| PedWait | https://anylogic.help/library-reference-guides/pedestrian-library/pedwait.html |
| PedService | https://anylogic.help/library-reference-guides/pedestrian-library/pedservice.html |
| PedSelectOutput | https://anylogic.help/library-reference-guides/pedestrian-library/pedselectoutput.html |
| Process Modeling Library | https://anylogic.help/library-reference-guides/process-modeling-library/index.html |
| ResourcePool | https://anylogic.help/library-reference-guides/process-modeling-library/resource-pool.html |
| Seize | https://anylogic.help/library-reference-guides/process-modeling-library/seize.html |
| Release | https://anylogic.help/library-reference-guides/process-modeling-library/release.html |

---

## Rules

1. **Always cite the doc URL** when explaining AnyLogic behavior or properties.
2. **Never guess** about property names, default values, or behavior — look it up.
3. **Quote the documentation** when the exact wording matters (e.g., what a property does).
4. **For the obstacle/walk-through problem**, the answer is always per the Rectangular Node docs:
   - Use `Wall` / `RectangularWall` for permanent obstacles (furniture, counters, walls).
   - Use `accessRestricted = true` + `accessRestrictionType = CONDITION` + `accessRestrictionCondition = true` + `avoidedIfClosed = true` on a `RectangleNode` to make it act as a pedestrian obstacle while still being reachable via `PedGoTo`/`PedWait`.
5. **Do not recommend workarounds** that contradict how the library is documented to work.
6. **For XML edits**, always verify against the `.alp` file structure first before making changes.

---

## Key Facts (from docs)

- **`RectangularWall`** → permanently impassable, no config needed. Use for physical structures.
- **`RectangleNode`** → walkable by default. Becomes obstacle only when `avoidedIfClosed = true` and the node is closed via access restriction.
- **`accessRestricted = true` alone does NOT make pedestrians avoid the node** — `avoidedIfClosed` must also be `true`.
- Nodes with access restrictions **change color to red** in the AnyLogic editor as a visual indicator.
- `PedGoTo` and `PedWait` that explicitly target a node will still send pedestrians into it even when access is restricted.
- **`PedWait` Routing:** `free(ped)` sends the pedestrian to the normal `out` port. `cancel(ped)` sends the pedestrian to the `ccl` (cancel) port. **If balking or cancelling a wait state group, always use `cancel(ped)` to bypass normal downstream flow (like table assignment).**
- **PedSelectOutput Condition Safety:** AnyLogic `PedSelectOutput` evaluates condition definitions multiple times. **Never mutate state (e.g. `trips--`) inside `condition` fields**, as it will cause dynamic choice changes resulting in runtime crashes (`choice changed before the agent transmission`). Always put mutating actions inside `onExit` actions instead.
- **Group Iteration:** `aGroup.iterator()` produces generic `Agent` references in AnyLogic. In order to process specific pedestrians logic, you must explicitly cast: `Customer c = (Customer) agent`.
- **XML Modification Safety:** AnyLogic autosaves frequently. Whenever manually modifying the `.alp` project XML file, the active project **must be completely closed** inside the AnyLogic IDE to prevent auto-save overwriting changes.
