import os

vecs = [
    ( 0, -1),
    (-1,  0),
    ( 0,  1),
    ( 1,  0),
]

turns = {
    (0, 1): '┐',
    (3, 2): '┐',
    (1, 0): '└',
    (2, 3): '└',
    (2, 1): '┘',
    (3, 0): '┘',
    (0, 3): '┌',
    (1, 2): '┌',

}
box_chars = {
    '-': '─',
    '|': '│',
    'L': '└',
    'J': '┘',
    '7': '┐',
    'F': '┌',
    '.': '█',
    'S': '░',
}

def dig(steps):
    min_x, min_y = 0, 0
    max_x, max_y = 0, 0
    x, y = 0, 0
    for d, s in steps:
        x += vecs[d][0] * s
        y += vecs[d][1] * s
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    start_x = -min_x
    start_y = -min_y
    w, h = max_x - min_x + 1, max_y - min_y + 1
    grid = [["█"] * w for _ in range(h)]
    x, y = start_x, start_y
    pd = None
    for i in range(len(steps)+1):
        d, s = steps[i%len(steps)]
        dx, dy = vecs[d]
        for _ in range(s):
            grid[y][x] = turns.get((pd, d), '─' if dy == 0 else '│')
            x += dx
            y += dy
            pd = d
    dug = 0
    for y, row in enumerate(grid):
        inside = False
        for x, c in enumerate(row):
            if c in "│└┘":
                inside = not inside
            elif c == "█" and inside:
                row[x] = (c := " ")
            if c != "█":
                dug += 1
        #print("".join(grid[y]))
    return dug

def dig2(steps):
    min_x, min_y = 0, 0
    x, y = 0, 0
    for d, s in steps:
        x += vecs[d][0] * s
        y += vecs[d][1] * s
        min_x = min(x, min_x)
        min_y = min(y, min_y)

    x, y = min_x, min_y
    double_area = 0
    dist = 0
    for d, s in steps:
        nx = x + vecs[d][0] * s
        ny = y + vecs[d][1] * s
        double_area += x*ny - nx*y
        dist += abs(nx-x) + abs(ny-y)
        x, y = nx, ny
    return abs(double_area//2) + dist//2+1

def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        dig_plan = [s.strip().split() for s in f.readlines()]

    steps = [("ULDR".index(step[0]), int(step[1])) for step in dig_plan]
    print(dig(steps))
    print(dig2(steps))
    steps = [("ULDR".index("RDLU"[int(step[2][7])]), int(step[2][2:7], base=16)) for step in dig_plan]
    print(dig2(steps))


base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")

