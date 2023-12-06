import os

def run(input_file):
    print(f"{input_file}:")

    seeds = []
    maps = []
    current_map = None

    with open(input_file, "r") as f:
        line = f.readline()
        if line[:7] != "seeds: ":
            raise Exception("expected seeds line")
        seeds = list(map(int, line[7:].split()))
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            if line[-4:] == "map:":
                current_map = []
                maps.append(current_map)
                continue
            [dst_start, src_start, length] = map(int, line.split())
            current_map.append((src_start, src_start + length, dst_start - src_start))

    for current_map in maps:
        current_map.sort()

    ranged_seeds = [(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
    #print(ranged_seeds)

    locations = []
    for val in seeds:
        for current_map in maps:
           for (a, b, offset) in current_map:
               if val in range(a, b):
                    val += offset
                    break
        locations.append(val)
    locations.sort()
    print(locations[0])

    locations = []
    #for val_range in ranged_seeds:
        #print("seed ", val_range)
    ranges = ranged_seeds
    for current_map in maps:
        #print("  current ranges ", ranges)
        mapped_ranges = []
        for (s2, e2, o) in current_map:
            #print("  map ", s2, e2, o)
            leftover = []
            for (s1, e1) in ranges:
                #print("    range ", s1, e1)
                (s, e) = (max(s1, s2) + o, min(e1, e2) + o)
                if s < e:
                    mapped_ranges.append((s, e))
                not_mapped = [
                    (s1, min(e1, s2)),
                    (max(s1, e2), e1),
                ]
                for (s, e) in not_mapped:
                    if s < e:
                        leftover.append((s, e))
            ranges = leftover
        ranges.extend(mapped_ranges)
    #print("  final ", ranges)
    ranges.sort()
    locations.append(ranges[0])
    locations.sort()
    print(locations[0][0])



today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")
