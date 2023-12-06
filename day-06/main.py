import os

def run(input_file):
    with open(input_file) as f:
        lines = [s.split(":")[1] for s in f.readlines()]
        races = zip(*(map(int, s.split()) for s in lines))
        p = 1
        for (e, r) in races:
            c = 0
            for t in range(0, e):
                d = t * (e - t)
                if d > r:
                    c += 1
            p *= c
        print(p)

        c = 0
        (e, r) = (int(s.replace(" ", "")) for s in lines)
        for t in range(0, e):
            d = t * (e - t)
            if d > r:
                c += 1
        print(c)

today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")

#d = t * (e - t)
#d > r
#r < t * (e - t)

