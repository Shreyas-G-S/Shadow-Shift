# Shadow Shift – Project Progress Report

## What has already been achieved

The core structure of the **Shadow Shift** game has been implemented. A grid-based maze has been created with walls, corridors, shadow zones, and interactive switches that toggle the shadow corridors.

The player agent can move through the maze manually and interact with switches that dynamically change shadow locations. Predator agents have been implemented with limited perception based on Manhattan distance and use a simple greedy pathfinding strategy to chase the player when the player is within their vision range.

The simulation loop has also been completed. The performance metric of the system is **survival time**, and the game ends either when the player is caught by a predator or survives the required time threshold. The **PEAS framework components** have therefore been successfully integrated into a working prototype.

---

## Immediate next steps

The next steps focus on improving the depth of agent behavior and game dynamics.

- Improve predator pathfinding so agents make more intelligent movement decisions instead of purely greedy choices.
- Implement limited search strategies such as **Breadth-First Search (BFS)** within the predator’s perception range.

---

## Challenges and adjustments

One challenge encountered is **balancing agent behavior** so that the game remains playable while still demonstrating emergent multi-agent dynamics.

Another adjustment involves the **shadow mechanic**. The current implementation toggles between two fixed shadow corridors, which works for demonstrating the concept but can limit strategic diversity.

---

## Plan for the next month

The project will proceed in four stages:

**Week 1**
- Improve predator decision-making.
- Refine movement rules for all agents.

**Week 2**
- Expand the dynamic shadow system.
- Add more environmental interactions.

**Week 3**
- Perform gameplay balancing.
- Testing and debugging to ensure stable agent interactions.

**Week 4**
- Finalize documentation.
- Demonstrate emergent behavior scenarios.
- Prepare the final project presentation.

---

## Final goal

Deliver a polished **multi-agent maze simulation** where simple local rules produce complex interactions between the player, predators, neutral agents, and the dynamic shadow environment.