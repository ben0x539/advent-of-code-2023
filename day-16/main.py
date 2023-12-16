import os

N,W,S,E = 0,1,2,3
vecs = [
    (-1,  0),
    ( 0, -1),
    ( 1,  0),
    ( 0,  1),
]

def trace(grid, i, j, d):
    h, w = len(grid), len(grid[0])
    paths = [[0 for _ in range(w)] for _ in range(h)]
    rays = [(i, j, d)]
    while len(rays) > 0:
        (i, j, d) = rays.pop()
        while True:
            di, dj = vecs[d]
            i, j = i + di, j + dj
            if i < 0 or i >= h or j < 0 or j >= w:
                break
            o = paths[i][j]
            b = 1 << d
            if (b & o) > 0:
                break
            paths[i][j] |= b
            match grid[i][j]:
                case '.':
                    pass
                case '|' if d in (W, E):
                        rays.append((i, j, (d+1)%4))
                        d = (d-1)%4
                case '-' if d in (N, S):
                        rays.append((i, j, (d+1)%4))
                        d = (d-1)%4
                case '/':
                    d = 3 - d
                case '\\':
                    d = (5 - d) % 4
            #for (ii, row) in enumerate(paths):
            #    for (jj, c) in enumerate(row):
            #        print('#' if c > 0 else grid[ii][jj], end='')
            #    print("")
            #print("")
    return sum(sum(1 if n > 0 else 0 for n in row) for row in paths)


def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        grid = list(map(str.strip, f.readlines()))
    h, w = len(grid), len(grid[0])
    energized = trace(grid, 0, -1, E)
    print(energized)
    best = 0
    for i in range(h):
        best = max(best, trace(grid, i, -1, E))
        best = max(best, trace(grid, i, w, W))
    for j in range(w):
        best = max(best, trace(grid, -1, j, S))
        best = max(best, trace(grid, h, j, N))
    print(best)

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")
