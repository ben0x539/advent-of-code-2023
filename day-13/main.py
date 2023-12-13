import os

def run(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        patterns = [pattern.split() for pattern in f.read().split("\n\n")]

    vertical_axes = []
    horizontal_axes = []
    post_smudge_vertical_axes = []
    post_smudge_horizontal_axes = []
    for pattern in patterns:
        pattern_post_smudge_vertical_axis = None
        pattern_post_smudge_horizontal_axis = None

        for j in range(1, len(pattern[0])):
            errs = 0
            for i in range(len(pattern)):
                row = pattern[i]
                w = min(j, len(row)-j)
                for x in range(w):
                    if row[j-1-x] != row[j+x]:
                        errs += 1
                        if errs >= 2:
                            break
            if errs == 0:
                vertical_axes.append(j)
            elif errs == 1 and pattern_post_smudge_vertical_axis is None:
                pattern_post_smudge_vertical_axis = j

        for i in range(1, len(pattern)):
            row = pattern[i]
            h = min(i, len(pattern)-i)
            errs = 0
            for j in range(len(row)):
                for x in range(h):
                    if pattern[i-1-x][j] != pattern[i+x][j]:
                        errs += 1
                        if errs >= 2:
                            break
            if errs == 0:
                horizontal_axes.append(i)
            elif errs == 1 and pattern_post_smudge_horizontal_axis is None:
                pattern_post_smudge_horizontal_axis = i

        if pattern_post_smudge_vertical_axis is not None:
            post_smudge_vertical_axes.append(pattern_post_smudge_vertical_axis)
        elif pattern_post_smudge_horizontal_axis is not None:
            post_smudge_horizontal_axes.append(pattern_post_smudge_horizontal_axis)

    print(sum(vertical_axes) + sum(horizontal_axes)*100)
    print(sum(post_smudge_vertical_axes) + sum(post_smudge_horizontal_axes)*100)



today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
#run(f"../inputs/custom-{today}.txt")
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")

