import os

class TransposedInner:
    def __init__(self, inner: list[list], row: int):
        self.inner = inner
        self.row = row

    def __getitem__(self, key):
        return self.inner[key][self.row]

    def __len__(self):
        return len(self.inner)

class Transposed:
    def __init__(self, inner: list[list]):
        self.inner = inner

    def __getitem__(self, key):
        return TransposedInner(self.inner, key)

    def __len__(self):
        return len(self.inner[0])

def run(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        patterns = [pattern.split() for pattern in f.read().split("\n\n")]

    total = 0
    total_smudge = 0
    for pattern in patterns:
        smudge_done = False
        for (f, mult) in [(lambda x: x, 1), (Transposed, 100)]:
            p = f(pattern)
            for j in range(1, len(p[0])):
                errs = 0
                for i in range(len(p)):
                    row = p[i]
                    w = min(j, len(row)-j)
                    for x in range(w):
                        if row[j-1-x] != row[j+x]:
                            errs += 1
                if errs == 0:
                    total += j * mult
                elif errs == 1 and not smudge_done:
                    smudge_done = True
                    total_smudge += j * mult

    print(total)
    print(total_smudge)

today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
#run(f"../inputs/custom-{today}.txt")
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")

