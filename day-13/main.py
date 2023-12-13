import os

def run(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        patterns = [pattern.split() for pattern in f.read().split("\n\n")]

    vertical_axes = []
    horizontal_axes = []
    #total = 0
    for pattern in patterns:
        #for j in range(1, len(pattern[0])):
        #    for i in range(len(pattern)):
        #        row = pattern[i]
        #        w = min(j, len(row)-j)
        #        left, right = row[j-w:j], row[j+w-1:j-1:-1]
        #        if left != right:
        #            break
        #    else:
        #        vertical_axes.append(j)

        #for i in range(1, len(pattern)):
        #    row = pattern[i]
        #    h = min(i, len(pattern)-i)
        #    for j in range(len(row)):
        #        up = [r[j] for r in pattern[i-h:i]]
        #        down = [r[j] for r in pattern[i+h-1:i-1:-1]]
        #        if up != down:
        #            break
        #    else:
        #        horizontal_axes.append(i)

        #for smudge_fixed in [False, True]:
        #    vertical_axes = []
        #    horizontal_axes = []

        #    print("\n".join(pattern))
        #    print("vertical")
        #    redo = False
        #    for j in range(1, len(pattern[0])):
        #        errs = []
        #        for i in range(len(pattern)):
        #            row = pattern[i]
        #            w = min(j, len(row)-j)
        #            for x in range(w):
        #                if row[j-1-x] != row[j+x]:
        #                    errs.append((j, i, j-1-x))
        #        if len(errs) == 0:
        #            vertical_axes.append(j)
        #        elif len(errs) == 1 and not smudge_fixed:
        #            i, j = errs[0][1:]
        #            print("fixing", i, j, pattern[i][j])
        #            pattern[i] = pattern[i][:j] + ".#"["#.".index(pattern[i][j])] + pattern[i][j+1:]
        #            redo = True
        #            break
        #    if redo:
        #        continue

        #    print("horizontal")
        #    for i in range(1, len(pattern)):
        #        row = pattern[i]
        #        h = min(i, len(pattern)-i)
        #        errs = []
        #        for j in range(len(row)):
        #            for x in range(h):
        #                if pattern[i-1-x][j] != pattern[i+x][j]:
        #                    errs.append((i, i-1-x, j))
        #        if len(errs) == 0:
        #            horizontal_axes.append(i)
        #        elif len(errs) == 1 and not smudge_fixed:
        #            i, j = errs[0][1:]
        #            print("fixing", i, j, pattern[i][j])
        #            pattern[i] = pattern[i][:j] + ".#"["#.".index(pattern[i][j])] + pattern[i][j+1:]
        #            redo = True
        #            break
        #    if redo:
        #        continue

        #    print(vertical_axes)
        #    print(horizontal_axes)
        #    total += sum(vertical_axes) + sum(horizontal_axes)*100
        #    break

        #print("\n".join(pattern))
        #print("vertical")
        done = False
        for j in range(1, len(pattern[0])):
            errs = []
            for i in range(len(pattern)):
                row = pattern[i]
                w = min(j, len(row)-j)
                for x in range(w):
                    if row[j-1-x] != row[j+x]:
                        errs.append((j, i, j-1-x))
            if len(errs) == 1:
                #print(j)
                vertical_axes.append(j)
                done = True
                break
        if done:
            continue

        #print("horizontal")
        for i in range(1, len(pattern)):
            row = pattern[i]
            h = min(i, len(pattern)-i)
            errs = []
            for j in range(len(row)):
                for x in range(h):
                    if pattern[i-1-x][j] != pattern[i+x][j]:
                        errs.append((i, i-1-x, j))
            if len(errs) == 1:
                #print(i)
                horizontal_axes.append(i)
                done = True
                break
        if done:
            continue

    print(vertical_axes)
    print(horizontal_axes)
    total = sum(vertical_axes) + sum(horizontal_axes)*100
    print(total)



today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
#run(f"../inputs/custom-{today}.txt")
#run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")

