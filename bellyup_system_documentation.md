# 🍽️ BellyUp Buffet Simulation System Documentation

This document outlines the core mechanics and logic implemented in the BellyUp Buffet AnyLogic simulation. It is designed to serve as a reference guide for future presentations or project handoffs.

## 1. System Overview

The simulation merges two underlying AnyLogic toolsets into one cohesive environment:
1. **Pedestrian Library (Green Blocks):** Tracks the physical movement, spacing, waiting, and routing of individual customers on the floor plan.
2. **Process Modeling Library (Blue Blocks):** Manages backend logistical processes, queues, and resources (Chefs, Waiters, and Table Turnover).

**Core Loop:** Customers consume resources (food and tables) $\rightarrow$ Trigger backend tasks based on thresholds $\rightarrow$ Staff (Waiters/Chefs) act to replenish those resources $\rightarrow$ Data is dynamically tracked and graphed.

---

## 2. Food Consumption Logic

Rather than tracking a single global "food level", the model records four distinct food lines independently to analyze popularity and varied drop rates.

- **Food Selection:** As customers enter the buffet line (`foodSelectionWaiting`), they are assigned a `foodChoice` identifier (0 = Seafood, 1 = Dimsum, 2 = Buffet, 3 = Beverage) using a probability distribution.
- **Consumption:** When customers finish at the station and trigger the *"On exit"* action, the system checks their `foodChoice` memory and subtracts exactly **1 unit** from the corresponding global food level variable.
- **Dynamic Charting:** A separate **Cyclic Event** acts as a heartbeat monitor. Every 1-simulation-minute, it pushes the 4 food levels to a `Dataset`, driving a real-time visual TimePlot chart. Waiter and Chef utilization levels are similarly pushed to a live Bar Chart.

---

## 3. The Preemptive Refill Strategy

The goal of the backend staff logic is to ensure the buffet never reaches 0 while keeping efficiency high.

### Thresholds & Boolean Guards
Refills are triggered preemptively when a food level hits **$\le$ 30 units** (out of 100).
However, 100 hungry customers walking by a low station could accidentally trigger 100 identical refill orders. To prevent this, we established **Boolean Guard Flags** (e.g., `seaFoodRefilling = true`). A station can only trigger an order if it is low AND not already being actively refilled.

### Solving the "Race Condition" Ticket System
Initially, the simulation used a single shared global variable (`refillStationIndex`) to tell the chefs what to cook. This caused a critical **Race Condition Bug**: If two stations ran low simultaneously, the second order overwrote the first order's variable while the chef was still cooking. The waiters would then mistakenly deliver both batches to the second station, leaving the first station permanently starved at 0.

**The Solution:**
We reused the `Customer` agent as a physical **"Refill Ticket"** inside the blue Process blocks:
1. When a station runs low, it calls `triggerRefill.inject(1)` and injects an agent into the Staff Flow.
2. The moment it drops into the flow, the agent snaps a copy of the target station index (0-3) and saves it into its own internal memory (`agent.foodChoice`).
3. The agent moves sequentially down the pipeline: `grabChef` $\rightarrow$ `cookingTime` $\rightarrow$ `grabWaiter` $\rightarrow$ `refillTray`.
4. As the agent finishes the delay inside `refillTray`, the code reads the agent's memory ticket, restores that exact station back to 100, and clears the Boolean guard flag.

*This elegantly decouples the work orders. Multiple refills can queue up concurrently without any data overwriting itself.*

---

## 4. Dynamic Seating and Group Assembly

Customers arrive as cohesive groups, separate to choose their food, and must re-assemble to eat at a correctly sized table.

- **The Waiting Room (`Hold` blocks):** Process Modeling `Hold` blocks act as a digital waiting room, configured in **Conditional Mode**. They seamlessly hold groups back at the entrance until the condition `!availableFourSeaters.isEmpty()` evaluates to true.
- **Table Assignment:** The exact moment a group is cleared to enter, they pop an available table node (e.g., a 4-seater or 10-seater) from a global List, ensuring nobody else can claim it. This is stored internally as `assignedTable`.
- **Group Assembly:** Once customers fill their plates, they navigate directly to their `assignedTable`. The `pedGroupAssemble` block forces the group to wait until everyone sits down together. To prevent total system deadlocks (where one stuck patron holds up an entire family forever), leniency timeouts or threshold conditions (e.g., 75% assembly) act as safety valves.
- **Returning the Table:** When the party finishes eating and exits, their specific `assignedTable` node is pushed back into the `availableFourSeaters` list, allowing the entrance Hold blocks to instantly release the next waiting party.
