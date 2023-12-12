import os

def add(options, springs, groups, weight):
    springs = springs.lstrip(".")
    for i, (s, g, w) in enumerate(options):
        if springs == s and groups == g:
            options[i] = (s, g, w+weight)
            return
    options.append((springs, groups, weight))

def try_combinations(springs, groups):
    valid = 0
    options = [(springs.strip("."), groups, 1)]
    i = 0
    while len(options) > 0:
        options.sort(key=lambda x: len(x[0]))
        (springs, groups, weight) = options.pop()
        #print(springs, groups)

        if len(groups) == 0:
            if springs.find("#") == -1:
                valid += weight
                #print("yay", weight)
            continue
        n = groups[0]
        if len(springs) < n:
            #print("abandoning")
            continue
        if springs[:n].find(".") == -1 and not (len(springs) >= n+1 and springs[n] == "#"):
            #print("consumed", options[-1])
            #options.append((springs[n+1:], groups[1:]))
            add(options, springs[n+1:], groups[1:], weight)
        if springs[0] != "#":
            #options.append((springs[1:], groups))
            add(options, springs[1:], groups, weight)
            #print("skipping to", options[-1])

    return valid

#def do_substitution(springs, v):
#    s = []
#    for c in springs:
#        if c == "?":
#            c = "#."[v&1]
#            v >>= 1
#        s.append(c)
#    return "".join(s)
#
#def is_valid(springs, groups):
#    for n in groups:
#        springs = springs.lstrip(".")
#        next_springs = springs.lstrip("#")
#        if n != len(springs) - len(next_springs):
#            #print("bad", springs, next_springs, n)
#            return False
#        springs = next_springs
#
#    if len(springs.lstrip(".")) > 0:
#        return False
#
#    return True

def run(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        records = [(springs, [int(group) for group in groups.split(",")])
            for [springs, groups] in
            (s.strip().split() for s in f.readlines())]

    total = 0
    for (springs, groups) in records:
        springs = "?".join([springs] * 5)
        groups = groups * 5
        valid_combos = try_combinations(springs, groups)
        #valid_combos = 0
        #unknowns = sum((int(c == "?") for c in springs))
        #for v in range(1<<unknowns):
        #    #print(unknowns, v)
        #    substituted_springs = do_substitution(springs, v)
        #    if is_valid(substituted_springs, groups):
        #        #print(substituted_springs, "ok")
        #        valid_combos += 1
        #    #else:
        #    #    print(substituted_springs, "bad")
        #print(springs, groups, valid_combos)
        total += valid_combos
    print(total)



today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")
