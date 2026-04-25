[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Rzy6ULC0)
# Lab 6: Sparse World Map

**Due Date:** April 10 at 11:59 pm
**Points:** 100 points
**Language:** Python

---

## Overview

In this lab you will implement a **sparse matrix** data structure and use it
to back the game's tile-based world map.

A **tile map** divides the world into a grid.  Each cell holds a tile ID
(a small integer).  In practice, most cells are empty (ID = -1), so storing
all `rows × cols` cells in a dense 2D array wastes memory.  A sparse matrix
stores *only* the non-empty entries — exactly as a dictionary would, but
using a data structure you build yourself.

By the end of this lab you will have:
- Designed your own world map using **Tiled** (a free map editor)
- Implemented a SparseMatrix class (DOK, COO, or CSR — your choice)
- Optionally implemented a HashTable to back your sparse matrix
- Adapted your enemy patrol routes to the new map
- Benchmarked your implementation against scipy and numpy

---

## Part 0: Copy over files from previous labs

Copy your implementations from earlier labs into lab-06:

```bash
cp lab_05/code/game/datastructures/waypoint.py    lab_06/code/game/datastructures/waypoint.py
cp lab_05/code/game/datastructures/patrol_path.py lab_06/code/game/datastructures/patrol_path.py
cp lab_05/code/game/datastructures/array.py       lab_06/code/game/datastructures/array.py
cp lab_05/code/game/datastructures/stack.py       lab_06/code/game/datastructures/stack.py
cp lab_05/code/game/time_travel.py                lab_06/code/game/time_travel.py
```

You also need to:
- Copy your `Character` subclasses into `lab_06/code/game/subcharacter.py` (from Lab 2)
- Copy your items into `create_example_items()` in `lab_06/code/game/item.py` (from Lab 3)
- Copy your character and enemy images

---

## Getting started

After completing Part 0, run the game to verify everything copied correctly:

```bash
cd code/game
python main.py YourName
```

You will see a black screen — that is expected.  The starter map CSV files
contain only -1 (empty) values, so no tiles are drawn yet.  The game still
launches and the character can move.

Once you implement SparseMatrix and replace the CSVs with your Tiled map,
the world will appear.

**Note:** The game will not launch if Part 0 is incomplete.  `inventory.py`
and `character.py` both depend on your `ArrayList` from Lab 3.

---

## Part 1: Design Your World Map (15 pts)

### What is Tiled?

**Tiled** is a free, open-source tile map editor available at
[mapeditor.org](https://www.mapeditor.org/).  It is widely used in indie
game development.

The game already uses the CSV export format that Tiled produces — that is
exactly what lives in `code/game/map/*.csv`.

### Install Tiled

Download from [mapeditor.org](https://www.mapeditor.org/) and install.
It is available for Windows, macOS, and Linux.

### Find tile art

You need a **tileset** — an image (or set of images) where each tile is
64 × 64 pixels.  Good free sources:
- [OpenGameArt.org](https://opengameart.org) — search "top-down tileset"
- [Itch.io](https://itch.io/game-assets/free/tag-top-down) — free assets
- [PixelLab](https://www.pixellab.ai) — AI pixel art generator, good for matching a consistent style
- AI-generated (Midjourney, Stable Diffusion, etc.)
- Hand-drawn in any pixel art editor (Piskel, Aseprite, etc.)

### Tiled workflow

1. **New map** -> Orientation: Orthogonal -> Tile size: 64 × 64
2. Set the map size (e.g. 60 columns × 40 rows — matching the starter CSVs)
3. **Tilesets** tab -> New Tileset -> load your tile image
4. **Layers** tab -> create three tile layers:
   - `FloorBlocks` — invisible collision walls and boundaries
   - `Grass` — ground cover (grass, sand, stone floor, etc.)
   - `Objects` — tall objects like trees, rocks, buildings
5. Paint your world.  Requirements:
   - At least **3 distinct areas** (e.g. forest, village, dungeon)
   - A consistent art style throughout
6. **File -> Export As** -> choose CSV -> export each layer separately:
   - `map_FloorBlocks.csv`
   - `map_Grass.csv`
   - `map_Objects.csv`
7. Copy the exported CSV files into `code/game/map/`, replacing the
   starter files.
8. For the floor background image, save a ground texture as
   `graphics/tilemap/ground.png`.

### Checklist for full marks

- [ ] At least 3 distinct areas with different tile themes
- [ ] Boundaries / walls mark the edges of each area
- [ ] The player starting position (tile 5, 5 by default) is inside a
      walkable area — move it in `level.py` if needed
- [ ] `ground.png` exists in `graphics/tilemap/`

---

## Part 2: Implement SparseMatrix (40 pts)

Open `code/game/datastructures/sparse_matrix.py`.

### Choose an implementation

Pick **one** of the three options.  All three must pass the same tests.

#### Option A: DOK — Dictionary of Keys
- Back the matrix with your **HashTable** (hash_table.py)
- `{ (row, col): value }` — like a dict but built by you
- Requires implementing HashTable (see Part 3)
- Average O(1) get/set

#### Option B: COO — Coordinate List
- Back the matrix with your **ArrayList** (array.py from Lab 3)
- Store entries as a list of `(row, col, value)` triples
- Simple to implement; get() is O(nnz) linear scan ("nnz" = number of non-zero elements)
- Do NOT use Python's built-in `list` inside SparseMatrix

#### Option C: CSR — Compressed Sparse Row
- Three parallel arrays: `row_ptr`, `col_idx`, `values`
- `row_ptr[i]` = index in col_idx/values where row i begins
- Very cache-friendly for row-wise access
- Most complex to implement

### Required interface

All implementations must provide:

```python
m = SparseMatrix(default=-1)
m.set(row, col, value)        # store; removes entry if value == default
m.get(row, col)               # returns stored value or default
m.items()                     # yields ((row, col), value) tuples
len(m)                        # number of stored entries
m.multiply(other)             # returns new SparseMatrix = self * other
str(m)                        # human-readable summary
```

### How the game uses your SparseMatrix

When you implement SparseMatrix, the game will automatically use it.
`support.py` calls `import_csv_to_sparse()` which tries to create a
SparseMatrix; if it raises `NotImplementedError`, it falls back to a
plain dict so the game still runs.

Once your SparseMatrix works, the tile map loads through your data
structure and the world renders correctly.

### Rule: no built-in list, dict, or set

You may NOT use Python's `dict` or `set` inside `SparseMatrix` or
`HashTable`.  You must use YOUR `ArrayList` inside COO or CSR.

---

## Part 3: Implement HashTable (optional — required for DOK)

**Only required if you chose Option A (DOK).**

Open `code/game/datastructures/hash_table.py`.

Your HashTable must provide:

```python
ht = HashTable(initial_capacity=64)
ht.set(key, value)            # insert or update
ht.get(key, default=None)     # lookup with fallback
ht.delete(key)                # remove; raises KeyError if absent
key in ht                     # __contains__
len(ht)                       # number of entries
ht.items()                    # yield (key, value) pairs
ht._hash(key)                 # your custom hash function
ht._resize()                  # double capacity and rehash
```

### Requirements

- Your `_hash()` must be your own implementation — do NOT call Python's
  `hash()` or use any built-in hashing.
- Handle collisions: chaining (list of lists or linked lists) or open addressing.
- Call `_resize()` when the **load factor** (len / capacity) exceeds 0.7.
- Keys will be `(row, col)` tuples — make sure your hash handles tuples.

---

## Part 4: Adapt Enemy Patrols (5 pts)

Open `code/game/enemy.py`.

The `ENEMY_SPAWN_DATA` list contains placeholder coordinates that were
reasonable for a generic map.  Now that you have designed your own map,
update the `spawn` and `waypoints` coordinates for each enemy so that:

- Each enemy starts inside a walkable area
- Patrol routes do not pass through walls or objects
- Routes make thematic sense (e.g. a Forest Guard patrols the forest)

You may add or remove enemies.  The minimum is **3 enemies with distinct patrol
routes**.  Keep at least one of each patrol type: circular, back_and_forth,
one_way.

Coordinates are in **tile units** (not pixels).  They are multiplied by
`TILESIZE = 64` at runtime.

---

## Part 5: Write Tests (10 pts)

Open `code/game/datastructures/tests/sparse_matrix_tests.py`.

The file already has five example tests.  Add at least **8 more** covering:

- All methods: `set`, `get`, `items`, `__len__`, `multiply`, `__str__`
- Edge cases: overwrite, set-to-default removes entry, empty matrix
- Large matrix: 1000 × 1000 with 10 entries
- Multiply: identity, zero matrix, hand-computed 2 × 2

Run your tests:

```bash
cd code/game/datastructures/tests
python sparse_matrix_tests.py
```

---

## Part 6: Complexity Analysis (15 pts)

### Step 1 — Create and run the simulation

```bash
cd code/game/datastructures/complexity
python sparse_matrix_complexity.py
```

Create and run your own simulations. Compare again the Scipy csr_matrix class, which is the standard sparse matrix implementation. I've already imported this for you, though you may need to install it. 

### Step 2 — Fill in the write-up

Open `code/game/datastructures/complexity/analysis_write_up.md` and fill
in:
- Your implementation choice and reasoning
- The theoretical time complexity of each operation
- The benchmark output (copy-paste from the terminal)
- Space complexity analysis
- Observations and conclusions

---

## Running the game

```bash
cd code/game
python main.py YourName
```

**Controls:**

| Key | Action |
|-----|--------|
| Arrow keys | Move |
| Space | Attack |
| I | Open inventory |
| R | Rewind (single-player) |
| F | Replay (single-player) |
| N | Toggle enemy debug view |
| M | Reset enemy patrols |
| Escape | Quit |

---

## Grading (100 points)

### Automated (20 pts)

| Test class | Points | What it tests |
|---|---|---|
| `TestSparseMatrixBasic` | 8 | set, get, default, len, items |
| `TestSparseMatrixEdge` | 5 | overwrite, set-to-default, consistency |
| `TestMatrixMultiply` | 7 | identity, basic 2x2, sparse result, zero matrix |

### Manual (80 pts)

| Category | Points | What is assessed |
|---|---|---|
| World map design (Part 1) | 20 | 3+ distinct areas, art, export quality |
| Complexity analysis (Part 6) | 20 | Benchmark run, analysis correct, write-up clear |
| Student-written tests (Part 5) | 15 | Coverage, edge cases, correctness |
| Analysis report (write-up) | 10 | Conclusions are thoughtful and accurate |
| Code documentation | 10 | Docstrings, comments, clean code |
| Enemy patrol updates (Part 4) | 5 | Coordinates updated, routes make sense |
| AI Discussions | 5 | Completed `ai_conversations.md` |

**Total: 100 points**

---

## Important rules

- Write your own docstrings for every method you implement.  The stubs
  intentionally leave them blank — documenting your code is part of the grade.
- Do **not** use Python's built-in `dict` or `set` inside `SparseMatrix`
  or `HashTable`.  (The autograder cannot enforce this, but your instructor
  will check during manual grading.)
- The game must launch even if your SparseMatrix is not yet implemented —
  `support.py` falls back to a plain dict automatically.
- The `SparseMatrix` interface is fixed.  Tests check the interface, not
  the internal representation.
- The `HashTable` (Part 3) is only required if you choose DOK.  There are
  no separate automated tests for `HashTable` — it is assessed through your
  SparseMatrix tests and manual code review.
