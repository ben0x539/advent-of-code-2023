import os

def hash(s):
    n = 0
    for c in s:
        n += ord(c)
        n *= 17
        n &= 0xff
    return n

def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        steps = f.read().strip().split(",")
    boxes = list(map(lambda _: [], range(256)))

    for step in steps:
        if step[-1] == "-":
            label = step[:-1]
            box = boxes[hash(label)]
            for i, (lens_label, _) in enumerate(box):
                if label == lens_label:
                    del box[i]
                    break
        else:
            label, focal = step.split("=", 2)
            focal = int(focal)
            box = boxes[hash(label)]
            for i, (lens_label, _) in enumerate(box):
                if label == lens_label:
                    box[i] = (label, focal)
                    break
            else:
                box.append((label, focal))
        
        print(f'After "{step}":')
        for (i, box) in enumerate(boxes):
            if len(box) != 0:
                contents = (f'[{l} {f}]' for (l, f) in box)
                print(f"Box {i}: {' '.join(contents)}")
        print("")

    total = sum(
        (sum(((1 + i) * (1 +j) * f for (j, (_, f)) in enumerate(box)))
         for (i, box)
         in enumerate(boxes)))
    print(total)

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")

