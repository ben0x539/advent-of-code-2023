import os
from dataclasses import dataclass

vecs = [
    ( 0, -1),
    (-1,  0),
    ( 0,  1),
    ( 1,  0),
]

@dataclass
class XYZRange:
    ends: tuple[tuple[int, int, int], tuple[int, int, int]]
    def __next__(sef):
        cur = self.ends[0]
        self.ends = (tuple(map(lambda x: x+1, ends[0]), ends[1]))
        return cur


@dataclass
class Brick:
    id: int
    ends: tuple[tuple[int, int, int], tuple[int, int, int]]

    def bottom(self):
        return self.ends[0][2]

    def is_backwards(self):
        return self.ends[0] > self.ends[1]

    def range(self):
        (x1, y1, z1), (x2, y2, z2) = self.ends
        while x1 <= x2:
            y = y1
            while y <= y2:
                z = z1
                while z <= z2:
                    yield x1, y, z
                    z += 1
                y += 1
            x1 += 1

    def below(self):
        (x1, y1, z1), (x2, y2, z2) = self.ends
        while x1 <= x2:
            y = y1
            while y <= y2:
                yield x1, y, z1-1
                y += 1
            x1 += 1

    def above(self):
        (x1, y1, z1), (x2, y2, z2) = self.ends
        while x1 <= x2:
            y = y1
            while y <= y2:
                yield x1, y, z2+1
                y += 1
            x1 += 1

    def move(self, dx, dy, dz):
        (x1, y1, z1), (x2, y2, z2) = self.ends
        self.ends = ((x1+dx, y1+dy, z1+dz), (x2+dx, y2+dy, z2+dz))

    def label(self):
        return chr(65 + self.id // 26) + chr(65 + self.id % 26)

    def __hash__(self):
        return self.id.__hash__()

class Bricks:
    def __init__(self, bricks):
        self.bricks = [Brick(n, ends) for n, ends in zip(range(99999), bricks)]
        w, d, h = 0, 0, 0
        for brick in self.bricks:
            #print("brick", brick.label(), brick)
            if brick.is_backwards():
                print("backwards:", brick)
            for (x, y, z) in brick.ends:
                w, d, h = max(x, w), max(y, d), max(z, h)
        w, d, h = w+1, d+1, h+1
        self.grid = [[[None for _ in range(w)] for _ in range(d)] for _ in range(h)]
        for brick in self.bricks:
            for x, y, z in brick.range():
                #print("brick", brick.label(), brick, x, y, z)
                self.grid[z][y][x] = brick

    def drop(self):
        while True:
            anything_changed = False
            for brick in self.bricks:
                try:
                    #print("checking to drop", brick.label(), brick)
                    while brick.bottom() > 1 and all(self.grid[z][y][x] == None for x, y, z in brick.below()):
                        #print("  has room below")
                        anything_changed = True
                        for x, y, z in brick.range():
                            self.grid[z][y][x] = None
                        brick.move(0, 0, -1)
                        for x, y, z in brick.range():
                            self.grid[z][y][x] = brick
                except Exception as e:
                    print("rip brick", brick)
                    raise
            if not anything_changed:
                break

    def get_supported(self, brick):
        supported = set()
        for x, y, z in brick.above():
            if z >= len(self.grid)-1:
                break
            b = self.grid[z][y][x]
            if b is not None:
                supported.add(b)
        return supported

    def get_supporting(self, brick):
        supporting = set()
        for x, y, z in brick.below():
            if z <= 0:
                break
            b = self.grid[z][y][x]
            if b is not None:
                supporting.add(b)
        return supporting

    def print(self):
        for z in range(len(self.grid)):
            z = len(self.grid) - z - 1
            level = self.grid[z]
            print("z =", z)
            for row in level:
                print(" ".join((".." if brick is None else brick.label()) for brick in row))
            print("")


def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        bricks = Bricks(tuple((tuple(map(int, b.split(","))) for b in s.strip().split("~"))) for s in f.readlines())
    #bricks.print()
    bricks.drop()
    #print("")
    #bricks.print()
    disintegratable = 0
    for brick in bricks.bricks:
        supports = bricks.get_supported(brick)
        if all(len(bricks.get_supporting(b)) > 1 for b in supports):
            #print("disintegrate", brick.label())
            disintegratable += 1
        #else:
            #print("don't disintegrate", brick.label(), list(map(Brick.label, supports)))
    print(disintegratable)

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")