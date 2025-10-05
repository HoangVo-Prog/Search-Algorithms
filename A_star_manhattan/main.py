from heapq import heappush, heappop
from itertools import count

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import START, GOAL 

# ---------- 8-puzzle A* with Manhattan ----------
N = 3
# Moves: Up, Down, Left, Right
DIRS = {'U': -N, 'D': N, 'L': -1, 'R': 1}
goal_index = {v: i for i, v in enumerate(GOAL)}

def is_solvable(state):
    arr = [x for x in state if x != 0]
    inv = sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i+1, len(arr)))
    # Với 3x3, trạng thái solvable khi số nghịch thế chẵn (goal hiện tại có 0 nghịch thế)
    return inv % 2 == 0

def manhattan(state):
    total = 0
    for i, v in enumerate(state):
        if v == 0: 
            continue
        gi = goal_index[v]
        r1, c1 = divmod(i, N)
        r2, c2 = divmod(gi, N)
        total += abs(r1 - r2) + abs(c1 - c2)
    return total

def neighbors(state):
    z = state.index(0)
    r, c = divmod(z, N)
    for mv, d in DIRS.items():
        nz = z + d
        if mv == 'U' and r == 0: continue
        if mv == 'D' and r == N-1: continue
        if mv == 'L' and c == 0: continue
        if mv == 'R' and c == N-1: continue
        lst = list(state)
        lst[z], lst[nz] = lst[nz], lst[z]
        yield tuple(lst), mv

def astar(start, goal=GOAL):
    if not is_solvable(start):
        return None, None, {"expanded": 0, "visited": 0}

    open_heap = []
    tie = count()
    g = {start: 0}
    parent = {start: None}
    move_taken = {start: None}
    h0 = manhattan(start)
    heappush(open_heap, (g[start] + h0, h0, next(tie), start))
    closed = set()
    expanded = 0

    while open_heap:
        f, h, _, s = heappop(open_heap)
        if s in closed:
            continue
        if s == goal:
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
            if tentative < g.get(ns, 10**9):
                g[ns] = tentative
                parent[ns] = s
                move_taken[ns] = mv
                hn = manhattan(ns)
                heappush(open_heap, (tentative + hn, hn, next(tie), ns))

    return None, None, {"expanded": expanded, "visited": len(g)}

# ------------- chạy thử -------------
if __name__ == "__main__":
    path, steps, stats = astar(START, GOAL)
    if path is None:
        print("Unsolvable puzzle")
    else:
        print("Moves:", path)         
        print("Step count:", steps)   
        print("Nodes expanded:", stats["expanded"])
        print("States generated:", stats["visited"])

    
