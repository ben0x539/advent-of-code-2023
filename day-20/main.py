import os
from collections import deque
#import re
#import typing
from dataclasses import dataclass

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
    state: dict[str, bool]

    def is_set(self):
        return all(v == 1 for v in self.state.values())

    def pulse(self, src, v):
        self.state[src] = v
        if all(v == 1 for v in self.state.values()):
            return self.send(0)
        else:
            return self.send(1)

@dataclass
class Counter:
    last_val: int
    unchanged_for: int
    change_at: list[int]

def run(input_file: str):
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
    n = None
    cycles = {}
    i = 0
    hist = {}
    pulse_hist = []
    max_len = 0
    state_hist = []
    #while True:
    for i in range(100000):
        signals.append(("broadcaster", "button", 0))
        lo, hi = 0, 0
        #if i < 4:
        #    print("round", i)
        ph = []
        pulse_hist.append(ph)
        while len(signals) > 0:
            m, src, v = signals.popleft()
            ph.append(v)
            if m == "rx" and v == 0 and n is None:
                n = i + 1
                print("n", n)
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
        #print("")
        vals = []
        #print(i)

        # rt:
        #   bs: 1
        #   mk: 2
        #   bt: 8
        #   vj: 32
        #   rr: 64
        #   zz: 256
        #   jg: 512
        #   vm: 1024
        #   pn: 1899??
        # gk:
        #   bz: 1
        #   rl: 16
        #   rh: 32
        #   vz: 256
        #   lg: 512
        #   rk: 1024
        #   sb: 1841??
        # fv:
        #for name, mod in modules.items():
            #if type(mod) == Conjunction:
                #if mod.is_set():
                #    if cycles.get(name) is None:
                #        cycles[name] = []
                #    cycles[name].append(i)
                #    #print(name, i)
                #vals.append(list(mod.state.values()))

                #for k, v in mod.state.items():
                #    n = f"{name}:{k}"
                #    if hist.get(n) is None:
                #        c = Counter(v, 1, [])
                #        hist[n] = c
                #    else:
                #        c = hist[n]
                #    if c.last_val == v:
                #        c.unchanged_for += 1
                #    else:
                #        c.last_val = v
                #        c.change_at.append((i, c.unchanged_for))
                #        c.unchanged_for = 1
                #vals.append(name+":"+"".join(map(str, mod.state.values())))
                #print(i, name, mod.state)
        #print(i, vals)
        sh = []
        state_hist.append(sh)
        for m in modules.values():
            if type(m) == FlipFlop:
                sh.append(m.state)
            elif type(m) == Conjunction:
                sh.extend(m.state.values())
        if len(ph) >= max_len:
            max_len = len(ph)
        #print("".join(map(str, ph)))
        print("".join(map(str, sh)))
        i += 1
    #for h in pulse_hist[:1000]:
    #    print("".join(map(str, h)))
    #for k, v in cycles.items():
    #    print(k, v[:20])
    print(lo_total, hi_total, lo_total*hi_total)
    print(n)
    print("")
    #for n, c in hist.items():
    #    print(n, c.change_at[:20])
        
base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
#run(f"{base}/inputs/sample-{today}.txt")
#run(f"{base}/inputs/sample-{today}-2.txt")
run(f"{base}/inputs/input-{today}.txt")

# &hj -> rx
#   &ks
#     &sl
#   &jf
#     &rt
#   &qs
#     &fv
#   &zk
#     &gk