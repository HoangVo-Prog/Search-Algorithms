from heapq import heappush, heappop
from itertools import count
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import START, GOAL 

# ---------- 8-puzzle A* with Manhattan + Linear Conflict ----------
N = 3
# Moves: Up, Down, Left, Right
DIRS = {'U': -N, 'D': N, 'L': -1, 'R': 1}
# For quick row/col and goal positions
goal_pos = {v: (i // N, i % N) for i, v in enumerate(GOAL)}

def is_solvable(state):
    """8-puzzle solvable iff inversion parity matches goal (blank ignored)."""
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    # Goal has 0 inversions parity ==> need even
    return inv % 2 == 0

def manhattan(state):
    """Sum of Manhattan distances to goal."""
    dist = 0
    for idx, v in enumerate(state):
        if v == 0: 
            continue
        r, c = divmod(idx, N)
        gr, gc = goal_pos[v]
        dist += abs(r - gr) + abs(c - gc)
    return dist

def linear_conflict(state):
    """Count linear conflicts in rows and cols; each adds 2 to heuristic."""
    lc = 0
    # rows
    for r in range(N):
        row = state[r*N:(r+1)*N]
        # tiles in their goal row
        tiles = [(c, t) for c, t in enumerate(row) if t != 0 and goal_pos[t][0] == r]
        # count inversions by goal column
        for i in range(len(tiles)):
            ci, ti = tiles[i]
            gi = goal_pos[ti][1]
            for j in range(i+1, len(tiles)):
                cj, tj = tiles[j]
                gj = goal_pos[tj][1]
                if gi > gj:
                    lc += 1
    # cols
    for c in range(N):
        col = [state[r*N + c] for r in range(N)]
        tiles = [(r, t) for r, t in enumerate(col) if t != 0 and goal_pos[t][1] == c]
        for i in range(len(tiles)):
            ri, ti = tiles[i]
            gi = goal_pos[ti][0]
            for j in range(i+1, len(tiles)):
                rj, tj = tiles[j]
                gj = goal_pos[tj][0]
                if gi > gj:
                    lc += 1
    return 2 * lc

def heuristic(state):
    return manhattan(state) + linear_conflict(state)

def neighbors(state):
    """Generate (next_state, move_char) pairs."""
    z = state.index(0)
    zr, zc = divmod(z, N)
    for m, delta in DIRS.items():
        nz = z + delta
        if m == 'U' and zr == 0: 
            continue
        if m == 'D' and zr == N-1: 
            continue
        if m == 'L' and zc == 0: 
            continue
        if m == 'R' and zc == N-1: 
            continue
        lst = list(state)
        lst[z], lst[nz] = lst[nz], lst[z]
        yield tuple(lst), m

def astar(start, goal=GOAL):
    if not is_solvable(start):
        return None, None, {"expanded": 0, "visited": 0}
    open_heap = []
    tie = count()
    g = {start: 0}
    parent = {start: None}
    move_taken = {start: None}
    h0 = heuristic(start)
    heappush(open_heap, (g[start] + h0, h0, next(tie), start))
    closed = set()
    expanded = 0
    while open_heap:
        f, h, _, s = heappop(open_heap)
        if s in closed:
            continue
        if s == goal:
            # reconstruct path
            path = []
            while move_taken[s] is not None:
                path.append(move_taken[s])
                s = parent[s]
            path.reverse()
            return ''.join(path), len(path), {"expanded": expanded, "visited": len(g)}
        closed.add(s)
        expanded += 1
        gs = g[s]
        for ns, mv in neighbors(s):
            if ns in closed:
                continue
            tentative = gs + 1
            if tentative < g.get(ns, 1_000_000_000):
                g[ns] = tentative
                parent[ns] = s
                move_taken[ns] = mv
                hn = heuristic(ns)
                heappush(open_heap, (tentative + hn, hn, next(tie), ns))
    return None, None, {"expanded": expanded, "visited": len(g)}

if __name__ == "__main__":
    path, steps, stats = astar(START, GOAL)
    if path is None:
        print("Unsolvable puzzle")
    else:
        print("Moves:", path)     
        print("Step count:", steps)
        print("Nodes expanded:", stats["expanded"])
        print("States generated:", stats["visited"])
