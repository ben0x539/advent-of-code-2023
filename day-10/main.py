import os

def find_s(grid):
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            if row[x] == "░":
                return (x, y)

def show(grid, cx, cy):
    #for y in range(max(cy-d, 0), min(cy+d, len(grid))):
    for y in range(len(grid)):
        row = grid[y]
        #for x in range(max(cx-d, 0), min(cx+d, len(row))):
        for x in range(len(row)):
            c = row[x]
            if (x, y) == (cx, cy):
                c = 'X'
            print(c, end='')
        print("")
    print("")

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

adjacent = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]

passable = {
    '─': [(0, -1), (0, 1)],
    '│': [(-1, 0), (1, 0)],
    '│': [(-1, 0), (1, 0)],
    '└': [(-1, 0), (0, 1)],
    '┘': [(-1, 0), (0, -1)],
    '┐': [(1, 0), (0, -1)],
    '┌': [(1, 0), (0, 1)],
    '█': [],
    '░': adjacent,
}

def boxify(s):
    return ''.join((box_chars[c] for c in s))

def flood_fill(grid, x, y, base_char, fill_char):
    stack = [(y, x)]
    i = 0
    while len(stack) > 0:
        y, x = stack.pop()
        if grid[y][x] != base_char:
            continue
        #show(grid, x, y)
        grid[y][x] = fill_char
        for (dx, dy) in adjacent:
            nx, ny = x + dx, y + dy
            if ny in range(len(grid)) and nx in range(len(grid[ny])) and grid[ny][nx] == base_char:
                stack.append((ny, nx))

def run(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        grid = [boxify(s.strip()) for s in f.readlines()]
        h = len(grid)
        w = len(grid[0])

        trace = [['█'] * w*3 for _ in range(h*3)]

        start_x, start_y = find_s(grid)
        x, y = start_x, start_y
        prev_x, prev_y = None, None
        steps = 0
        while not (steps > 0 and (x, y) == (start_x, start_y)):
            #show(grid, x, y)
            for (dy, dx) in adjacent:
                nx, ny = x + dx, y + dy
                if nx in range(w) and ny in range(h) and (nx, ny) != (prev_x, prev_y) and (dy, dx) in passable[grid[y][x]] and (-dy, -dx) in passable[grid[ny][nx]]:
                    #print("moving", (dx, dy), grid[ny][nx], passable)
                    prev_x, prev_y = x, y
                    trace[y*3+1+dy][x*3+1+dx] = '░'
                    x, y = nx, ny
                    trace[y*3+1-dy][x*3+1-dx] = '░'
                    trace[y*3+1][x*3+1] = '░'
                    steps += 1
                    break
            else:
                raise Exception('stuck', (x, y), [grid[y+dy][x+dx] for ((dy, dx), _) in adjacent])
        #show(grid, x, y)
        #show(trace, x*3, y*3)
        print(steps - steps//2)
        flood_fill(trace, 0, 0, '█', ' ')
        show(trace, x*3+1, y*3+1)
        enclosed = 0
        for y in range(1, len(trace), 3):
            for x in range(1, len(trace[y]), 3):
                if trace[y][x] == '█':
                    enclosed += 1
        print(enclosed)


today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/sample-{today}-2.txt")
run(f"../inputs/input-{today}.txt")
