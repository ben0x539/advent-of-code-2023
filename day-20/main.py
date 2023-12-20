import sys
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
    state: dict[str, int]

    def is_set(self):
        #print(self.name, list(self.state.values()))
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
    presses_before_rx = None
    cycles = {}
    i = 0
    hist = {}
    pulse_hist = []
    max_len = 0
    state_hist = []
    #while True:
    e=1000000
    for i in range(1000000):
        if i % 1000 == 0:
            print(f"\r               \r{i*100/e}%", file=sys.stderr, end="")
        signals.append(("broadcaster", "button", 0))
        lo, hi = 0, 0
        #if i < 4:
        #    print("round", i)
        ph = []
        pulse_hist.append(ph)
        while len(signals) > 0:
            m, src, v = signals.popleft()
            ph.append(v)
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
        #print("")
        vals = []
        #print(i)
        for name, mod in modules.items():
            if type(mod) == FlipFlop:
                v = mod.state
                if hist.get(name) is None:
                    c = Counter(v, 1, [])
                    hist[name] = c
                else:
                    c = hist[name]
                if c.last_val == v:
                    c.unchanged_for += 1
                else:
                    c.last_val = v
                    c.change_at.append((i, c.unchanged_for, v))
                    c.unchanged_for = 1
                vals.append(name+":"+str(mod.state))
            if type(mod) == Conjunction:
                #v = mod.is_set()
                #if hist.get(name) is None:
                #    c = Counter(v, 1, [])
                #    hist[name] = c
                #else:
                #    c = hist[name]
                #if c.last_val == v:
                #    c.unchanged_for += 1
                #else:
                #    c.last_val = mod.state
                #    c.change_at.append((i, c.unchanged_for, v))
                #    c.unchanged_for = 1

                #if mod.is_set():
                #    if cycles.get(name) is None:
                #        cycles[name] = []
                #    cycles[name].append(i)
                    #print(name, i)
                #vals.append(list(mod.state.values()))

                for k, v in mod.state.items():
                    n = f"{name}:{k}"
                    if hist.get(n) is None:
                        c = Counter(v, 1, [])
                        hist[n] = c
                    else:
                        c = hist[n]
                    if c.last_val == v:
                        c.unchanged_for += 1
                    else:
                        c.change_at.append((i, c.unchanged_for, v))
                        c.last_val = v
                        c.unchanged_for = 1
                vals.append(name+"["+",".join(f"{k}:{v}" for k, v in mod.state.items()))
                #print(i, name, mod.state)
        print(i, " ".join(vals))
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
        #print("".join(map(str, sh)))
        i += 1
    #for h in pulse_hist[:1000]:
    #    print("".join(map(str, h)))
    #for k, v in cycles.items():
    #    print(k, v[:20])
    print("", file=sys.stderr)
    print(lo_total, hi_total, lo_total*hi_total)
    print(presses_before_rx)
    print("")
    for n, c in hist.items():
        print(n)
        last_period = None
        changes = 0
        for (i, period, val) in c.change_at:
            if i < 10 or last_period != period:
                print("  ", i, period, val)
                if period != last_period:
                    last_period = period
                    changes += 1
                    if changes > 8:
                        break
        
base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
#run(f"{base}/inputs/sample-{today}.txt")
#run(f"{base}/inputs/sample-{today}-2.txt")
run(f"{base}/inputs/input-{today}.txt")

# &hj -> rx
#   &ks
#     &sl
#       rq 1,2,0 2,1,1 3,1,0, 4,1,1
#       dc 2047,2048,1 4012,1965,0 6060,2048,1 8025,1965,0, 10073,2048,1
#       ql 7,8,1 15,8,0 23,8,1 31,8,0 39,8,1 47,8,0
#       jl 511,512,1 1024,512,0 1535,512,1 2047,512,0... 11609,512,1 12038,429,0... 7x512,429, 413
#       mr 1024,1024,1 2047,1024,0 3071,1024,1 4012,941, 0 3x1024,941, 4013
#       jc 31,32,1 63,32,0 ... 4012,13,0
#       gv ... 256,.. 4012,173,0
#       mm period 4
#       cc period 128... 4012,45
#   &jf
#     &rt
#   &qs
#     &fv
#   &zk
#     &gk


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