import os

vecs = [
    ( 0, -1),
    (-1,  0),
    ( 0,  1),
    ( 1,  0),
]

def go(garden: list[str], steps: int) -> int:
    h, w = len(garden), len(garden[0])
    (i, j), = ((i, r.find("S")) for i, r in enumerate(garden) if "S" in r)
    #print(i, j)
    points = set([(i, j)])
    next_points = set()
    while steps > 0:
        #k = 0
        #for (i, j) in points:
        #    print((i+j)%2, (i, j))
        #    k += 1
        #    if k == 32:
        #        break
        for i, j in points:
            for di, dj in vecs:
                ni, nj = i + di, j + dj
                #if ni >= 0 and ni < h and nj >= 0 and nj < w and garden[ni][nj] != "#":
                if garden[ni % h][nj % w] != "#":
                    next_points.add((ni, nj))
        if steps == 1:
        #    for i in range(-h*9, h*10):
        #        row = garden[i % h]
        #        if i % h == 0:
        #            print("")
        #        for j in range(-w*9, w*10):
        #            if j % w == 0:
        #                print(" ", end="")
        #            c = row[j % w]
        #            if (i, j) in next_points:
        #                c = 'O'
        #            print(c, end='')
        #        print("")
        #    print("")

            def count_grid(ii, jj):
                c = 0
                for i in range(h*ii, h*(ii+1)):
                    for j in range(w*jj, w*(jj+1)):
                        if (i, j) in next_points:
                            c += 1
                return c
            #print("origin", count_grid(0, 0)) # 7354
            #print("south", count_grid(1, 0)) # 7362
            #print("west", count_grid(0, -3)) # 5558
            #print("east", count_grid(0, 3)) # 5538

            for ii in range(-4, 5):
                for jj in range(-4, 5):
                  print(f"({ii}, {jj})={count_grid(ii, jj)}", end="    ")
                print("\n")

            #print(max(next_points, key=lambda a: a[0]))
            #print(max(next_points, key=lambda a: a[1]))
            #print("total", len(next_points))
            return len(next_points)
        #print(steps, len(next_points), len(next_points) - len(points))
        points = next_points
        next_points = set()
        steps -= 1
    return len(points)


def run(input_file: str, steps: int):
    print("steps", steps)
    #with open(input_file, "r", encoding="utf-8") as f:
    #    garden = [s.strip() for s in f.readlines()]
    #r1 = go(garden, steps)
    #print("measured", r1)

    g_000001_1 = 925 # top left side small
    g_011111_0 = 6459 # top left side big

    g_000100_1 = 937 # top right side small
    g_110111_0 = 6444 # top right side big

    g_001000_1 = 936 # bottom left side small
    g_111011_0 = 6461 #bottom left side big

    g_010111_0 = 5541 # top

    g_111111_1 = 7354 # full neighbor
    g_111111_0 = 7362 # full origin (at 4)

    g_111110_0 = 6456 # bottom right big
    g_100000_1 = 941 # bottom right small

    g_011011_0 = 5558 # left
    g_110110_0 = 5538 # right

    g_111010_0 = 5555 # bottom

    s = steps // 131

    r2 = g_011011_0 + g_110110_0 # left right
    r2 += g_111010_0 + g_010111_0 + g_000001_1 + g_000100_1 + g_001000_1 + g_100000_1 # top/bottom/small corners

    r2 += (s - 1) * (g_000001_1 + g_011111_0 + g_110111_0 + g_000100_1 + g_001000_1 + g_111011_0 + g_100000_1 + g_111110_0) + s*s * g_111111_1 + (s-1)*(s-1) * g_111111_0

    print("computed", r2)
    #print("diff", r1 - r2)

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
#run(f"{base}/inputs/sample-{today}.txt", steps=6)
#run(f"{base}/inputs/sample-{today}.txt", steps=10)
#run(f"{base}/inputs/sample-{today}.txt", steps=50)
#run(f"{base}/inputs/sample-{today}.txt", steps=100)
#run(f"{base}/inputs/sample-{today}.txt", steps=500)
run(f"{base}/inputs/input-{today}.txt", steps=131*1 + 26501365 % 131)
run(f"{base}/inputs/input-{today}.txt", steps=131*2 + 26501365 % 131)
run(f"{base}/inputs/input-{today}.txt", steps=131*3 + 26501365 % 131)
run(f"{base}/inputs/input-{today}.txt", steps=131*4 + 26501365 % 131)
run(f"{base}/inputs/input-{today}.txt", steps=26501365)

