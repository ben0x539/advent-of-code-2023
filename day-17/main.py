import os
import time
from heapq import *

vecs = [
    (-1,  0),
    ( 0, -1),
    ( 1,  0),
    ( 0,  1),
]

def dist(grid, pos, end):
    (pi, pj), (ei, ej) = pos, end
    return abs(pi - ei) + abs(pj - ej)

def reconstruct_path(came_from, current):
    total_path = [current]
    while True:
        current = came_from.get(current)
        if current is None:
            break
        total_path.append(current)
    return total_path

def astar(grid, start, end):
    w, h = len(grid[0]), len(grid)
    cf = dist(grid, start, end)
    current = (start, 2, 0)
    open_set = set([(cf, current)])
    kill_set = set()
    open_heap = [(cf, current)]
    came_from = {}
    g_score = {}
    g_score[current] = 0
    f_score = {}
    f_score[current] = cf

    counter = 0
    while len(open_set) > 0:
        if counter == 1000:
            grid_ = [list(row) for row in grid]
            for _, ((i, j), d, _) in open_set:
                grid_[i][j] = "^<v>"[d]
            print("\033[2J" + "\n".join("".join(row) for row in grid_), "\n", len(open_set))
            counter = 0
            time.sleep(0.020)
        else:
            counter += 1

        cf, current = heappop(open_heap)
        while (cf, current) in kill_set:
            kill_set.remove(cf, current)
            cf, current = heappop(open_heap)
        open_set.remove((cf, current))

        if current[0] == end and current[2] >= 4:
            path = reconstruct_path(came_from, current)
            grid = [list(row) for row in grid]
            for (i, j), d, _ in path:
                grid[i][j] = "^<v>"[d]
            print("\033[2J")
            for row in grid:
                print("".join(row))
            return [pos for pos, d, s in path][:-1]

        (i, j), d, s = current

        #dirs = [(d-1)%4, (d+1)%4]
        #if s < 3:
        #    dirs.append(d)
        dirs = []
        if s == 0:
            dirs = [3] # ugh
        if s >= 4:
            dirs = [(d-1)%4, (d+1)%4]
        if s < 10:
            dirs.append(d)
        for dd in dirs:
            di, dj = vecs[dd]
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= h or nj < 0 or nj >= w:
                continue
            ss = s
            if dd != d:
                ss = 0
            neighbor = ((ni, nj), dd, ss+1)
            gs = g_score[current] + int(grid[ni][nj])
            ngs = g_score.get(neighbor, None)
            if not ngs or gs < ngs:
                came_from[neighbor] = current
                g_score[neighbor] = gs
                nf = gs + dist(grid, (ni, nj), end)
                of = f_score.get(neighbor)
                if of and of != nf:
                    open_set.remove((of, neighbor))
                    kill_set.add((of, neighbor))
                f_score[neighbor] = nf
                found = False
                if (nf, neighbor) not in open_set:
                    #if ss+1 >= 4:
                    #    for os in range(4, ss+1):
                    #        if ((ni, nj), dd, os+1) in open_set:
                    #            break
                    #    else:
                    #        open_set.add(neighbor)
                    #        for os in range(ss+1, 10):
                    #            o = ((ni, nj), dd, os+1)
                    #            if o in open_set:
                    #                open_set.remove(o)
                    #else:
                        open_set.add((nf, neighbor))
                        if (nf, neighbor) in kill_set:
                            kill_set.remove((nf, neighbor))
                        else:
                            heappush(open_heap, (nf, neighbor))
                    #heappush(open_set, neighbor)
    return None


def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        grid = list(map(str.strip, f.readlines()))

    path = astar(grid, (0, 0), (len(grid)-1, len(grid[0])-1))
    print(sum(int(grid[i][j]) for i, j in path))

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/sample-{today}-2.txt")
run(f"{base}/inputs/input-{today}.txt")

