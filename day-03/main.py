def issymbol(c: str):
    return not c.isalnum() and not c.isspace() and c != '.'

lines = None
#with open("../inputs/sample-day-03.txt") as f:
with open("../inputs/input-day-03.txt") as f:
    lines = f.readlines()

adjacent_coords = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

parts_sum = 0
for i in range(len(lines)):
    line = lines[i].strip()
    j = 0
    while j < len(line):
        #p = j
        #while p < len(line) and line[p].isdigit():
        #    p += 1
        #if p > j:
        #    a = max(j-1, 0)
        #    b = min(p+1, len(line));
        #    surrounding = line[a:b]
        #    if i > 0:
        #       surrounding += "\n" + lines[i-1][a:b]
        #    if i < len(line)-1:
        #       surrounding += "\n" + lines[i+1][a:b]
        #    if any(map(issymbol, surrounding)):
        #        #print("found", line[j:p], "\n", surrounding)
        #        parts_sum += int(line[j:p])
        #    j = p
        #else:
        #    j += 1
        c = line[j]
        if c != '*':
            j += 1
            continue

        adjacent_nums = []
        for (di, dj) in adjacent_coords:
            i_, j_ = i + di, j + dj
            if not i_ in range(len(lines)):
                continue
            line_ = lines[i_]
            if not j_ in range(len(line_)):
                continue
            if not line_[j_].isdigit():
                continue
            if dj >= 0 and j_ > 0 and line_[j_-1].isdigit():
                continue
            a, b = j_, j_ + 1
            while a > 0 and line_[a-1].isdigit():
                a -= 1
            while b < len(line_) and line_[b].isdigit():
                b += 1
            adjacent_nums.append(line_[a:b])
        if len(adjacent_nums) == 2:
            parts_sum += int(adjacent_nums[0]) * int(adjacent_nums[1])
        j += 1

print(parts_sum)
