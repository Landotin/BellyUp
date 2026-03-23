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
