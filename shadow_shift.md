

Project Proposal: Shadow Shift – A Multi-Agent Grid Game
## Sai Dheekshit Reddy Antham, Shreyas Gutti Srinivas, Prasanna Adarsh Kolli
## Overview
Shadow Shift is a grid-based maze game inspired by Pac-Man, where the player navigates a dynamic
maze shared with multiple autonomous agents.  The focus is on emergent behavior, as each agent
acts  independently  based  on  local  perception  and  simple  rules.   Players  must  strategically  use
shadows and corridors to avoid threats and survive as long as possible.
PEAS Framework
-  Performance:  Player survival time and successful avoidance of enemy agents.
-  Environment:  Grid-based maze with corridors, dynamic lighting, and moving obstacles.
-  Actuators:  Player/agent movement; switches to manipulate shadow zones.
-  Sensors:  Limited perception of nearby tiles, obstacles, and other agents.
## Objectives
-  Navigate the maze safely while avoiding predators.
-  Use shadows and environmental elements to create safe paths.
-  React to dynamically moving agents without global maze knowledge.
Agent Roles and Rules
-  Player:  Moves manually, reacts to threats, manipulates switches to control shadow areas.
-  Predator Agents:  Chase the player using local perception and pathfinding; avoid overlapping.
-  Neutral Agents:  Wander randomly, unintentionally blocking paths and affecting dynamics.
## Goal
Survive  in  the  maze  as  long  as  possible  while  navigating  multi-agent  interactions  and  dynamic
shadow zones, demonstrating emergent behavior from simple agent rules.
## 1