import os

def run(path):
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        instructions = ["LR".index(c) for c in f.readline().strip()]
        f.readline()
        for line in f.readlines():
            label, left, right = line[0:3], line[7:10], line[12:15]
            graph[label] = (left, right)
    print(path)
    print("part 1")
    if graph.get("AAA") is None:
        print("no AAA in input, skipping")
    else:
        pos = "AAA"
        step = 0
        while pos != "ZZZ":
            pos = graph[pos][instructions[step % len(instructions)]]
            step += 1
        print(step)

    print("part 2")

    #print(instructions)
    keys = [k[::-1] for k in graph.keys()]
    keys.sort()
    #print(keys)
    graph_indexes = [
        (keys.index(l[::-1]), keys.index(r[::-1]))
        for (l, r)
        in (graph[k[::-1]] for k in keys)
    ]
    #print(graph_indexes)
    for (i, k) in enumerate(keys):
        if k[0] != "A":
            n = i
            break

    for start in range(n):
        print("start", start)
        pos = start
        step = 0
        last_end = None
        while not (step > 0 and pos == start) and step < 1000000:
            pos = graph_indexes[pos][instructions[step % len(instructions)]]
            step += 1
            if pos >= len(keys)-n:
                d = None
                if last_end is not None:
                    d = step - last_end
                print("end", pos, step, d)
                last_end = step
            if graph_indexes[pos] == (pos, pos):
                print("stuck")
                break
        print("loop", step)

    #and then i went to wolfram alpha


    #step = 0
    #poses = list(range(n))
    #print(poses)
    #while not all((p >= len(keys)-n for p in poses)):
    #    instruction = instructions[step % len(instructions)]
    #    for (i, pos) in enumerate(poses):
    #        poses[i] = graph_indexes[pos][instruction]
    #    if step % 1000000 == 0:
    #        print(step, poses)
    #    step += 1
    #print(step)

today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
#run(f"../inputs/sample-{today}.txt")
#run(f"../inputs/sample-{today}-2.txt")
run(f"../inputs/input-{today}.txt")
