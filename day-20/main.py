import sys
import os
from collections import deque
#import re
#import typing
from dataclasses import dataclass

counter = 0
important = ["zk", "qs", "jf", "ks"]

@dataclass
class Module:
    name: str
    dests: list[str]

    def send(self, v):
        return [(dest, self.name, v) for dest in self.dests]

@dataclass
class Broadcaster(Module):
    def pulse(self, src, v):
        return self.send(v)


@dataclass
class FlipFlop(Module):
    state: int

    def pulse(self, src, v):
        if v == 1:
            return []
        self.state = 1 - self.state
        if self.state:
            return self.send(1)
        else:
            return self.send(0)

@dataclass
class Conjunction(Module):
    state: dict[str, int]

    def is_set(self):
        #print(self.name, list(self.state.values()))
        return all(v == 1 for v in self.state.values())

    def pulse(self, src, v):
        global counter
        self.state[src] = v
        p = 1
        if all(v == 1 for v in self.state.values()):
            p = 0
        if p == 1 and self.name in important:
            print(f"i={counter} n={self.name} p={p}")
        return self.send(p)

        #else:
        #    return self.send(1)

@dataclass
class Counter:
    last_val: int
    unchanged_for: int
    change_at: list[int]

def run(input_file: str):
    global counter
    print(f"{input_file}:")
    with open(input_file, "r", encoding="utf-8") as f:
        modules_str = list(map(str.strip, f.readlines()))
    modules = {}
    broadcaster = None
    for line in modules_str:
        left, _, right = line.partition(" -> ")
        dests = right.split(", ")
        ty = None
        if left == "broadcaster":
            ty = "broadcaster"
        else:
            ty, left = left[0], left[1:]
        m = None
        match ty:
            case "broadcaster":
                m = Broadcaster(left, dests)
            case "%":
                m = FlipFlop(left, dests, 0)
            case "&":
                m = Conjunction(left, dests, {})
        modules[left] = m
    for name, mod in modules.items():
        for d in mod.dests:
            if d == "output":
                continue
            dest = modules.get(d)
            if dest is not None and type(dest) == Conjunction:
                dest.state[name] = 0
    
    signals = deque()
    lo_total, hi_total = 0, 0
    presses_before_rx = None
    i = 0
    #e=1000000
    #for i in range(1000000):
    while True:
        counter = i
        #print(f"{counter}, {i}")
        #if i % 10000 == 0:
            #print(f"\r                  \r{i}", file=sys.stderr, end="")
        signals.append(("broadcaster", "button", 0))
        lo, hi = 0, 0
        #if i < 4:
        #    print("round", i)
        while len(signals) > 0:
            m, src, v = signals.popleft()
            if m == "rx" and v == 0 and presses_before_rx is None:
                presses_before_rx = i + 1
                print("presses_before_rx", presses_before_rx)
            if v == 0:
                lo += 1
            else:
                hi += 1
            #if i < 4:
            #    print(f"  {src} -{['low','high'][v]}-> {m}")
            mod = modules.get(m)
            if mod is not None:
                r = mod.pulse(src, v)
                signals.extend(r)
        #if i < 4:
        #    print(lo, hi)
        lo_total += lo
        hi_total += hi
        i += 1
    print("", file=sys.stderr)
    print(lo_total, hi_total, lo_total*hi_total)
    print(presses_before_rx)
    print("")
        
base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
#run(f"{base}/inputs/sample-{today}.txt")
#run(f"{base}/inputs/sample-{today}-2.txt")
run(f"{base}/inputs/input-{today}.txt")