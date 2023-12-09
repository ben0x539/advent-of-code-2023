import os

def run(input_file):
    with open(input_file) as f:
        lines = f.readlines()

    nexts = []
    prevs = []
    for line in lines:
        numbers = [int(s) for s in line.split()]
        numberses = [numbers]
        while any((n != 0 for n in numbers)):
            numbers = [a - b for (a, b) in zip(numbers[1:], numbers[:-1])]
            numberses.append(numbers)
        nexts.append(sum((ns[-1] for ns in numberses)))
        prev = 0
        for n in (ns[0] for ns in numberses[::-1]):
            prev = n - prev
        prevs.append(prev)
    print(sum(nexts))
    print(sum(prevs))


today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")
