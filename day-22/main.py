import os
import copy
from collections import deque
from dataclasses import dataclass
import cProfile

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
        sorted_bricks = list(bricks)
        sorted_bricks.sort(key=lambda b: b[0][2])
        self.bricks = [Brick(n, ends) for n, ends in enumerate(sorted_bricks)]
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
        dropped = set()
        while True:
            anything_changed = False
            for brick in self.bricks:
                dropped_this_one = False
                while brick.bottom() > 1 and all(self.grid[z][y][x] == None for x, y, z in brick.below()):
                    if not dropped_this_one:
                        dropped.add(brick.id)
                        dropped_this_one = True
                    anything_changed = True
                    for x, y, z in brick.range():
                        self.grid[z][y][x] = None
                    brick.move(0, 0, -1)
                    for x, y, z in brick.range():
                        self.grid[z][y][x] = brick
            if not anything_changed:
                break
        return dropped

    def drop_from(self, zapped):
        gone = set([None, zapped])

        relevant = list(self.get_supported(zapped))
        i = 0
        while i < len(relevant):
            brick = relevant[i]
            i += 1
            if brick in gone:
                continue
            for b in self.get_supporting(brick):
                if b not in gone:
                    break
            else:
                for b in self.get_supported(brick):
                    if b not in gone:
                        relevant.append(b)
                gone.add(brick)
        return len(gone) - 2

    def get_supported(self, brick):
        found = set()
        for x, y, z in brick.above():
            if z >= len(self.grid)-1:
                break
            b = self.grid[z][y][x]
            if b is not None:
                found.add(b)
        return found

    def get_supporting(self, brick):
        found = set()
        for x, y, z in brick.below():
            if z <= 0:
                break
            b = self.grid[z][y][x]
            if b is not None:
                found.add(b)
        return found

    #def zap(self, brick):
    #    for x, y, z in brick.range():
    #        self.grid[z][y][x] = None
    #    del self.bricks[brick.id]
    #    return brick

    def copy(self):
        other = Bricks(())
        other.bricks = self.bricks.copy()
        other.grid = self.grid.copy()
        return other

    #def print(self):
    #    for z in range(len(self.grid)):
    #        z = len(self.grid) - z - 1
    #        level = self.grid[z]
    #        print("z =", z)
    #        for row in level:
    #            print(" ".join((".." if brick is None else brick.label()) for brick in row))
    #        print("")


def run(input_file: str):
    print(input_file)
    with open(input_file, "r", encoding="utf-8") as f:
        bricks = Bricks(tuple((tuple(map(int, b.split(","))) for b in s.strip().split("~"))) for s in f.readlines())
    #bricks.print()
    bricks.drop()
    #print("")
    #bricks.print()
    disintegratable = 0
    for brick in bricks.bricks:
        supports = bricks.get_supported(brick)
        if all(sum(1 for b in bricks.get_supporting(b)) > 1 for b in supports):
            #print("disintegrate", brick.label())
            disintegratable += 1
        #else:
            #print("don't disintegrate", brick.label(), list(map(Brick.label, supports)))
    print(disintegratable)

    total = 0
    for brick in bricks.bricks:
        dropped = bricks.drop_from(brick)
        total += dropped
        print(f"zapped {brick.label()}, {dropped} dropped")
    print(total)

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
#cProfile.run('run(f"{base}/inputs/sample-{today}.txt")')
#cProfile.run('run(f"{base}/inputs/input-{today}.txt")', sort="cumulative")
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")
