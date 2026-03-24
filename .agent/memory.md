# BellyUp — Bug Memory Log

Track bugs encountered during development and how they were resolved.

---

## Bug #1 — Pedestrians Walking Through 3D Objects

**Date:** 2026-03-24
**Status:** ✅ Fixed

### Problem
Customers walk through 3D physical objects in the buffet (counters, buffet island, wall dividers, tables) as if they don't exist.

### Root Cause
In AnyLogic's Pedestrian Library, 3D visual shapes (`Figure3D`, Box3D) have **zero effect** on pedestrian pathfinding. Only `Wall`, `RectangularWall`, and `RectangleNode` with `avoidedIfClosed = true` are treated as obstacles.

The `table4seater` `RectangleNode`s (58 total) use `AreaNodeDescriptor` with no access restriction — pedestrians freely walk through them.

### Fix
**For tables (`table4seater` nodes × 58):**
Set the following on each node's `AreaNodeDescriptor` parameters:
- `accessRestricted` → `true`
- `accessRestrictionType` → `CONDITION`
- `accessRestrictionCondition` → `true`
- `avoidedIfClosed` → `true`

This makes pedestrians route *around* the table while still allowing assigned customers to enter via `PedGoTo`/`PedWait`.

**For buffet counters and island (permanent obstacles):**
Add `RectangularWall` elements matching the position/size of each 3D object.

**Doc Reference:** [Rectangular Node](https://anylogic.help/markup/node-r-ped.html)

> Actual fix used: `accessRestricted=true` + `capacity=0` + `avoidedIfClosed=true`
> Setting `capacity=0` means the node is permanently "full" → always closed → pedestrians avoid it.
> `self.CONDITION` enum failed — see Bug #3.
> 
> **⚠️ UPDATE (2026-03-24): This fix CAUSED Bug #4.**
> Setting `avoidedIfClosed = true` and `capacity=0` turns the ENTIRE table node (including its attractors) into a permanent obstacle. When pedestrians are forced to wait there via `PedWait`, they treat the seat as an obstacle, causing them to clump at the edges and fail to occupy unique attractors.
> 
> **Revised Fix for Bug #1:** Remove `accessRestricted`, `avoidedIfClosed`, and `capacity` overrides from the `table4seater` nodes entirely. To prevent walking through tables, draw a physical `RectangularWall` over the un-walkable center of the table (the wood/metal), leaving the bounding `RectangleNode` and its attractors walkable.

---

## Bug #3 — Wrong Enum Constant: `self.CONDITION` Not a Field

**Date:** 2026-03-24
**Status:** ✅ Fixed

### Problem
AnyLogic threw: `CONDITION cannot be resolved or is not a field` when the patched `.alp` was loaded. The patch script had injected `self.CONDITION` as the value for `accessRestrictionType`.

### Root Cause
`self.CONDITION` is not a valid Java field on the `IAreaNodeDescriptor` type. The correct enum constant name was not available in the documentation; `AreaAccessRestrictionType.CONDITION` exists in Java but cannot be referenced via `self.` shorthand in this context.

### Fix
Restored the file from the pre-patch backup, then re-ran the patch script using a different strategy:
- **Left `accessRestrictionType` empty** (defaults to `capacity` mode)
- **Set `capacity = 0`** — the node is always full → always closed
- **Set `avoidedIfClosed = true`** — pedestrians route around the closed node

This avoids the enum entirely and achieves the same obstacle behavior.

**Doc Reference:** [Rectangular Node – Properties](https://anylogic.help/markup/node-r-ped.html#properties)
> *capacity: "As long as the number of agents is less than or equal to Capacity, access is granted."* With capacity=0, no agent can passively enter.

---

## Bug #2 — `ped.myGroupSize` NullPointerException

**Date:** 2026-03-24
**Status:** ✅ Fixed

### Problem
`ped.myGroupSize` caused errors because it was stored as a custom variable and computed in the `onExit` of `PedSource`, but the group may not yet exist at that point.

### Fix
- Removed the `myGroupSize` variable from the `Customer` agent
- Removed the `onExit` code that set `ped.myGroupSize`
- Changed the `condition1` in `pedSelectOutput` from `ped.myGroupSize <= 4` to:
  ```java
  ped.getGroup() == null || ped.getGroup().size() <= 4
  ```
  This evaluates group size safely at the moment it's needed.

**Doc Reference:** https://anylogic.help/library-reference-guides/pedestrian-library/pedselectoutput.html

**Doc Reference:** https://anylogic.help/library-reference-guides/pedestrian-library/pedselectoutput.html

---

## Bug #4 — Customers Clumping and Ignoring Attractors

**Date:** 2026-03-24
**Status:** ✅ Fixed

### Problem
Customers were all clumping at the exact same table (the first one) instead of distributing evenly. Additionally, multiple agents were stuck grouping together on the edges of the table node and failing to stand on their unique attractors (seats), while blocking other pedestrians from crossing nearby.

### Root Cause
Two separate issues:
1. **Seating Selection:** The `seize4` block `onSeizeUnit` used `availableFourSeaters.remove(0)`. This always grabbed the first available table from the list, meaning all customers were funneled to whichever table was at index 0.
2. **Attractor Obstacle Blockage:** The fix for **Bug #1** turned the entire `table4seater` `RectangleNode` into an obstacle (`capacity=0`, `avoidedIfClosed=true`). When `PedWait` forced an agent into that obstacle node, the pathfinder prevented them from fully entering to reach their designated attractor.

### Fix
1. **Distribution:** Changed `onSeizeUnit` to randomize table assignment:
   `agent.assignedTable = availableFourSeaters.remove(uniform_discr(0, availableFourSeaters.size() - 1));`
   *(Note: The user had actually independently patched this in a recent commit, but the seating issue remained due to the obstacle definition).*
2. **Attractors:** Removed `accessRestricted=true`, `capacity=0`, and `avoidedIfClosed=true` from all **58** `table4seater` nodes in the `.alp` file using a Python patch script. The nodes are now fully walkable, meaning customers can pathfind instantly to their attractor seats.
3. *Note:* To stop people walking through the physical table centers, `RectangularWall` shapes must be manually drawn in the AnyLogic editor (as originally recommended).

**Doc Reference:** 
- [PedWait](https://anylogic.help/library-reference-guides/pedestrian-library/pedwait.html)
- [Attractors](https://anylogic.help/markup/attractor-ped.html)

---

## Template for new bugs

## Bug #N — Short Description

**Date:** YYYY-MM-DD
**Status:** 🔍 In Progress / ✅ Fixed / ❌ Workaround

### Problem
What happened and where.

### Root Cause
Why it happened.

### Fix
What was changed to resolve it.

**Doc Reference:** URL
