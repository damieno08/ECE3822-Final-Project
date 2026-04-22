[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/nXRNob0L)
# Lab 5: NPC Patrol Paths with Linked Lists

**Due Date:** April 3 at 11:59 pm
**Points:** 100 points
**Language:** Python

---

## Overview

In this lab, you'll implement **linked list data structures** to create NPC (Non-Player Character) patrol systems for your game. NPCs will follow patrol paths defined by linked lists, demonstrating practical applications of:

- **Singly Linked Lists** (one-way patrols)
- **Circular Linked Lists** (looping patrols) 
- **Doubly Linked Lists** (back-and-forth patrols)

Your NPCs will patrol around the expanded game world.

---

## Part 0: Copy over files from previous labs

Copy your implementations from earlier labs into lab-05:

```bash
cp lab_03/code/game/datastructures/array.py  lab_05/code/game/datastructures/array.py
cp lab_04/code/game/datastructures/stack.py  lab_05/code/game/datastructures/stack.py
cp lab_04/code/game/time_travel.py           lab_05/code/game/time_travel.py
```

You also need to:
- Copy your `Character` subclasses into `lab_05/code/game/subcharacter.py` (from Lab 2)
- Copy your items into `create_example_items()` in `lab_05/code/game/item.py` (from Lab 3)
- Copy any custom graphics into the `graphics/` folder

**Note:** If copying old code causes any issues, come to office hours and we can debug together.

---

## Getting Started

### **First Run (Before Implementation):**

1. **Run the game first** to see the expanded world:
   ```bash
   cd code/game
   python main.py
   ```

2. **What you'll see:**
   - Expanded 40×30 world map with distinct regions
   - No moving NPCs yet (they need your implementations!)
   - Message: "No NPCs active - implement Waypoint and PatrolPath classes!"

3. **Press 'N'** to toggle debug view - you'll see the message about needing implementations

### **Implementation Order:**

#### **Step 1: Implement Waypoint Class**
- File: `code/game/datastructures/waypoint.py`
- This is the **node** class for your linked lists
- Stores position (x, y) and links to other waypoints

#### **Step 2: Implement PatrolPath Class**  
- File: `code/game/datastructures/patrol_path.py`
- This is the **linked list** class
- Supports three patrol types: one_way, circular, back_and_forth

#### **Step 3: Test Your Implementation**
1. Run unit tests:
   ```bash
   cd code/game/datastructures/tests
   python linked_list_tests.py
   ```

2. Run the game again:
   ```bash
   cd code/game
   python main.py
   ```

3. **You should now see 5 NPCs** moving around with different patrol patterns!

#### **Step 4: Debug & Visualize**
- **Press 'N':** Toggle NPC debug visualization (shows patrol paths, target waypoints)
- **Press 'M':** Reset all NPC patrols to start positions

#### **Step 5: Analysis & Polish**
1. Complete complexity analysis
2. Add NPC sprites
3. Write analysis report

---

## Expanded Game World

The world map has been expanded to **40×30 tiles** with distinct regions:

```
Regions:
├── Forest (northwest) - Guarded by Forest Guard
├── Village (northeast) - Merchant patrols market 
├── Temple (center) - Priest walks meditation path
├── Dungeon (southeast) - Scout guards entrance
└── Market (east) - Vendor arranges goods
```

---

## NPC Patrol Behaviors

Each NPC demonstrates a different linked list type:

### 1. **Forest Guard** (Circular Linked List)
- **Path:** Rectangular patrol around forest perimeter
- **Implementation:** Circular linked list where tail connects back to head

### 2. **Village Merchant** (Doubly Linked List) 
- **Path:** Back-and-forth in village square
- **Implementation:** Doubly linked list with forward/backward traversal

### 3. **Temple Priest** (Circular Linked List)
- **Path:** Small meditation circle around temple
- **Implementation:** Circular linked list with longer wait times

### 4. **Dungeon Scout** (Singly Linked List)
- **Path:** One-way path to dungeon entrance  
- **Implementation:** Singly linked list with termination

### 5. **Market Vendor** (Doubly Linked List)
- **Path:** Back-and-forth arranging market goods
- **Implementation:** Doubly linked list with commercial purpose

---

## 🛠️ What You Need to Implement

### **File 1: `datastructures/waypoint.py` (10 points)**
```python
class Waypoint:
    def __init__(self, x, y, wait_time=0):
        # TODO: Store position, wait_time, next/prev pointers
    
    def distance_to(self, other_x, other_y):
        # TODO: Calculate Euclidean distance
```

### **File 2: `datastructures/patrol_path.py` (30 points)**
```python
class PatrolPath:
    def add_waypoint(self, x, y, wait_time=0):
        # TODO: Add waypoint to linked list
    
    def get_next_waypoint(self):
        # TODO: Return next waypoint based on patrol type
```

### **File 3: `datastructures/complexity/linked_list_complexity.py` (15 points)**
```python
# TODO: Complete performance analysis comparing linked lists vs arrays
```

---

## 🎮 Testing Your Implementation

### **1. Unit Tests**
```bash
cd code/game/datastructures/tests
python linked_list_tests.py
```

### **2. Visual Testing**
```bash
cd code/game
python main.py
# Press 'N' for debug view
# Press 'M' to reset patrols
```

### **3. Performance Analysis**
```bash
cd code/game/datastructures/complexity  
python linked_list_complexity.py
```

---

## 🎨 NPC Sprites (5 points)

Create or find sprites for your 5 NPCs:
- **Size:** 32×32 pixels
- **Format:** PNG with transparency  
- **Style:** Top-down view
- **Sources:** AI-generated, OpenGameArt.org, Itch.io, or hand-drawn

---

## Grading (100 points)

### Automated (20 pts)

| Test class | Points | What it tests |
|---|---|---|
| `TestWaypoint` | 5 | Initialization, distance, pointers |
| `TestPatrolPathBasic` | 3 | Init, add_waypoint, size, is_empty |
| `TestPatrolPathOneWay` | 4 | One-way traversal, stops at end |
| `TestPatrolPathCircular` | 4 | Circular wrap-around |
| `TestPatrolPathBackAndForth` | 3 | Direction reversal at endpoints |
| `TestPatrolPathReset` | 1 | Reset returns to head |

### Manual (80 pts)

| Category | Points | What is assessed |
|---|---|---|
| Testing | 20 | Unit test coverage, edge cases, correctness |
| Complexity Analysis | 20 | Benchmark run, analysis correct, write-up clear |
| Analysis Report | 15 | Conclusions are thoughtful and accurate |
| Documentation | 10 | Docstrings, comments, clean code |
| NPC Sprites | 10 | Custom sprites added, visually distinct |
| AI Discussions | 5 | Completed `ai_conversations.md` |

**Total: 100 points**