import os

N,W,S,E = 0,1,2,3
vecs = [
    (-1,  0),
    ( 0, -1),
    ( 1,  0),
    ( 0,  1),
]

def trace(grid, i, j, d, escaped):
    h, w = len(grid), len(grid[0])
    paths = [[0 for _ in range(w)] for _ in range(h)]
    rays = [(i, j, d)]
    while len(rays) > 0:
        (i, j, d) = rays.pop()
        while True:
            di, dj = vecs[d]
            i, j = i + di, j + dj
            if i < 0:
                escaped[0][j] = 1;
                break
            if i >= h:
                escaped[1][j] = 1;
                break
            if j < 0:
                escaped[2][i] = 1;
                break
            if j >= w:
                escaped[3][i] = 1;
                break
            #if i < 0 or i >= h or j < 0 or j >= w:
            #    escaped[(i, j)] = 1
            #    break
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
    #for row in paths:
    #    for n in row:
    #        c = ' ' if n == 0 else '#'
    #        print(c, end="")
    #    print("")
    return sum(sum(1 if n > 0 else 0 for n in row) for row in paths)


def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        grid = list(map(str.strip, f.readlines()))
    h, w = len(grid), len(grid[0])
    #energized = trace(grid, 0, -1, E, {})
    #print(energized)

    escaped_left = [0]*h
    escaped_right = [0]*h
    escaped_up = [0]*w
    escaped_down = [0]*w
    escaped = (escaped_up, escaped_down, escaped_left, escaped_right)

    best = 0
    for i in range(h):
        if not escaped_left[i]:
            best = max(best, trace(grid, i, -1, E, escaped))
        if not escaped_right[i]:
            best = max(best, trace(grid, i, w, W, escaped))
    for j in range(w):
        if not escaped_up[j]:
            best = max(best, trace(grid, -1, j, S, escaped))
        if not escaped_down[j]:
            best = max(best, trace(grid, h, j, N, escaped))
    print(best)

    #print(max(e for g in (
    #   *((trace(grid, i, -1, E, escaped), trace(grid, i, w, W, escaped)) for i in range(h)),
    #   *((trace(grid, -1, j, S, escaped), trace(grid, h, j, N, escaped)) for j in range(w)),
    #) for e in g))

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")
