import os

def show(image):
    for row in image:
        print(row)

def run(input_file):
    #part1(input_file)
    part2(input_file)

def part1(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        image = [s.strip() for s in f.readlines()]

    i = 0
    while i < len(image):
        if all((c == "." for c in image[i])):
            image.insert(i, "." * len(image[i]))
            i += 1
        i += 1

    h = len(image)

    i = 0
    while i < len(image[0]):
        if all((image[j][i] == "." for j in range(h))):
            for j in range(h):
                image[j] = image[j][:i] + "." + image[j][i:]
            i += 1
        i += 1

    #show(image)

    nodes = []
    for (i, row) in enumerate(image):
        for (j, c) in enumerate(row):
            if c == '#':
                nodes.append((i, j))

    ds = 0
    c = 0
    for (i1, j1) in nodes:
        for (i2, j2) in nodes:
            if (i1, j1) >= (i2, j2):
                continue
            c += 1
            di = abs(i1 - i2)
            dj = abs(j1 - j2)
            ds += di + dj
            print((i1, j1), (i2, j2), di + dj)

    print(c, ds)


def part2(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        image = [s.strip() for s in f.readlines()]

    gap_rows = [i for (i, row) in enumerate(image) if all((c == "." for c in row))]
    gap_cols = [j for j in range(len(image[0])) if all((row[j] == "." for row in image))]

    nodes = []
    for (i, row) in enumerate(image):
        for (j, c) in enumerate(row):
            if c == '#':
                nodes.append((i, j))

    for expansion in [1, 9, 99, 1_000_000-1]:
        ds = 0
        c = 0
        for (o, (i1, j1)) in enumerate(nodes):
            for (i2, j2) in nodes[o+1:]:
                #if (i1, j1) >= (i2, j2):
                #    continue
                j1_, j2_ = sorted([j1, j2])
                c += 1
                di = i2 - i1
                dj = j2_ - j1_
                for i3 in gap_rows:
                    if i3 >= i2:
                        break
                    if i3 > i1:
                        di += expansion
                for j3 in gap_cols:
                    if j3 >= j2_:
                        break
                    if j3 > j1_:
                        dj += expansion
                ds += di + dj
                #print((i1, j1), (i2, j2), di + dj)

        print(c, ds)


today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")
