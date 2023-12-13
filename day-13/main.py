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

    vertical_axes = []
    horizontal_axes = []
    post_smudge_vertical_axes = []
    post_smudge_horizontal_axes = []
    for pattern in patterns:
        pattern_post_smudge_vertical_axes = []
        pattern_post_smudge_horizontal_axes = []

        for (f, a, s_a) in [(lambda x: x, vertical_axes, pattern_post_smudge_vertical_axes), (Transposed, horizontal_axes, pattern_post_smudge_horizontal_axes)]:
            p = f(pattern)
            for j in range(1, len(p[0])):
                errs = 0
                for i in range(len(p)):
                    row = p[i]
                    w = min(j, len(row)-j)
                    for x in range(w):
                        if row[j-1-x] != row[j+x]:
                            errs += 1
                            if errs >= 2:
                                break
                if errs == 0:
                    a.append(j)
                elif errs == 1:
                    s_a.append(j)

        if len(pattern_post_smudge_vertical_axes) > 0:
            post_smudge_vertical_axes.append(pattern_post_smudge_vertical_axes[0])
        elif len(pattern_post_smudge_horizontal_axes) > 0:
            post_smudge_horizontal_axes.append(pattern_post_smudge_horizontal_axes[0])

    print(sum(vertical_axes) + sum(horizontal_axes)*100)
    print(sum(post_smudge_vertical_axes) + sum(post_smudge_horizontal_axes)*100)



today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
#run(f"../inputs/custom-{today}.txt")
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")

