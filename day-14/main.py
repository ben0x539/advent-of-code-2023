import os

N,W,S,E = 0,1,2,3
vecs = [
    (-1,  0),
    ( 0, -1),
    ( 1,  0),
    ( 0,  1),
]
#def tilt_(platform: list[str], direction: int):
#    di, dj = vecs[direction]
#    di_, dj_ = vecs[(direction-1)%4]
#    si = (len(platform) - 1) * ((1 + di - di_) // 2)
#    sj = (len(platform[0]) - 1) * ((1 + dj - dj_) // 2)
#
#    print(di, dj)
#    print(di_, dj_)
#    print(si, sj)
#    print(si + di_, sj + dj_)
#    print("")
#
#p = [["."]*10]*10
#tilt_(p, 0)
#tilt_(p, 1)
#tilt_(p, 2)
#tilt_(p, 3)
#exit()

def tilt(platform: list[str], direction: int):
    di, dj = vecs[direction]
    di_, dj_ = vecs[(direction-1)%4]
    si = (len(platform) - 1) * ((1 + di - di_) // 2)
    sj = (len(platform[0]) - 1) * ((1 + dj - dj_) // 2)

    i, j = si, sj
    bi, bj = None, None
    while i in range(0, len(platform)) and j in range(0, len(platform[0])):
        show(platform, [(i, j), (bi, bj), (si, sj)])
        print("")
        c = platform[i][j]
        if c == '#':
            bi, bj = None, None
        elif bi is None or bj is None:
            bi, bj = i, j
        if c == 'O':
            platform[i][j], platform[bi][bj] = platform[bi][bj], c
            bi, bj = bi - di, bj - dj
            print("swap!")

        i, j = i - di, j - dj
        if i not in range(0, len(platform)) or j not in range(0, len(platform[0])):
            si, sj = si + di_, sj + dj_
            i, j = si, sj
            bi, bj = None, None

def find(items, item):
    return next((i for (i, v) in enumerate(items) if v == item), None)

def show(platform: list[str], special: list[tuple[(int, int)]] = []):
    for (i, row) in enumerate(platform):
        for (j, c) in enumerate(row):
            p = find(special, (i, j))
            if p is not None:
                c = f"\033[{91+p}m{c}\033[0m"
            print(c, end="")
        print("")

def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        platform = [[c for c in s.strip()] for s in f.readlines()]

    while True:
        show(platform)
        print("")
        cmd = input("dir> ")
        if cmd == "":
            break
        direction = "NWSE".index(cmd.strip())
        tilt(platform, direction)

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
#run(f"../inputs/custom-{today}.txt")
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")

