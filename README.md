# 🧭 Search Algorithms

A collection of pathfinding algorithms implemented in Python, including optimized A* variants.

---

## ⚙️ Configuration

You can configure the **start** and **goal** positions in `config.py`:

```python
# config.py
START = (x_start, y_start)
GOAL = (x_goal, y_goal)
```

## 🚀 How to Run

```bash
# Run standard A* with Manhattan heuristic
python ./A_star_manhattan/main.py

# Run A* with Linear Conflict heuristic
python ./A_star_manhattan_linear_conflict/main.py
```

## Results

```bash
# A* with Manhattan

Moves: LURDDLURRULLDRRDLLURRULDLU
Step count: 26
Nodes expanded: 1480
States generated: 2306
```

```bash
#  A* with Manhattan + Linear Conflict

Moves: LURDDLURRULLDRRDLLURRULDLU
Step count: 26
Nodes expanded: 835
States generated: 1315
```