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
class Output(Module):
    def pulse(self, src, v):
        pass

@dataclass
class Counter:
    last_val: int
    unchanged_for: int
    change_at: list[int]

def run(input_file: str):
    #print(f"{input_file}:")
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
    modules["rx"] = Output("rx", [])

    print("""
#include <stdio.h>

unsigned long counter = 0;
unsigned long pulse_counters[2] = {0,0};
""")
    inputs = {}
    for name, mod in modules.items():
        for d in mod.dests:
            if d == "output":
                continue
            dest = modules.get(d)
            if dest is not None and type(dest) == Conjunction:
                inputs.setdefault(dest.name, []).append(name)
    for conj, srcs in inputs.items():
        print(f"enum Inputs_{conj} {{")
        for src in srcs:
            print(f"  SLOT_{conj}_{src},")
        print(f"  SLOT_{conj}_COUNT")
        print("};")
    for name, mod in modules.items():
        if type(mod) == FlipFlop:
            print(f"static void {name}(int v);")
        if type(mod) == Conjunction:
            print(f"static void {name}(int v, int slot);")
        if type(mod) == Broadcaster:
            print(f"static void {name}(int v);")
    print("static void rx(int v);")
    for name, mod in modules.items():
        if type(mod) == FlipFlop:
            print(f"static void {name}(int v) {{")
            print("    ++pulse_counters[v];")
            print("    static int state = 0;")
            print("    if (v == 1) return;")
            print("    state = 1 - state;")
            for d in mod.dests:
                dest = modules[d]
                if type(dest) == FlipFlop or type(dest) == Output:
                    print(f"    {dest.name}(state);")
                elif type(dest) == Conjunction:
                    print(f"    {dest.name}(state, SLOT_{dest.name}_{name});")
            print("}")
        if type(mod) == Conjunction:
            print(f"static void {name}(int v, int slot) {{")
            print("    ++pulse_counters[v];")
            print(f"    static int state[SLOT_{name}_COUNT] = {{0}};")
            print(f"    int i, all_set = 1;")
            print(f"    state[slot] = v;")
            print(f"    for (i = 0; i < SLOT_{name}_COUNT; ++i) {{")
            print("        if (state[i] != 1) {")
            print("            all_set = 0;")
            print("            break;")
            print("        }")
            print("    }")
            for d in mod.dests:
                dest = modules[d]
                if type(dest) == FlipFlop or type(dest) == Output:
                    print(f"    {dest.name}(1 - all_set);")
                elif type(dest) == Conjunction:
                    print(f"    {dest.name}(1 - all_set, SLOT_{dest.name}_{name});")
            print("}")
        if type(mod) == Broadcaster:
            print(f"static void {name}(int v) {{")
            print("    ++pulse_counters[v];")
            for d in mod.dests:
                dest = modules[d]
                if type(dest) == FlipFlop or type(dest) == Output:
                    print(f"    {dest.name}(v);")
                elif type(dest) == Conjunction:
                    print(f"   {dest.name}(v, SLOT_{dest.name}_{name});")
            print("}")
    print("")
    print("""
        static void rx(int v) {
            ++pulse_counters[v];
            if (v == 0) {
                printf("low pulse sent to rx at i = %lu\\n", counter);
            }
        }

        int main(void) {
            while (++counter < (1lu<<63)) {
                if (counter % 10000 == 0)
                    printf("%lu\\n", counter);
                if (counter == 1001) {
                    printf("pulses %lu, %lu\\n", pulse_counters[0], pulse_counters[1]);
                }
                broadcaster(0); 
            }

            return 0;
        }
    """);

    #for name, mod in modules.items():
    #    for d in mod.dests:
    #        if d == "output":
    #            continue
    #        dest = modules.get(d)
    #        if dest is not None and type(dest) == Conjunction:
    #            dest.state[name] = 0
    #signals = deque()
    #lo_total, hi_total = 0, 0
    #presses_before_rx = None
    #i = 0
    #while True:
    #    if i % 100000 == 0:
    #        print(f"\r                                    \r{i}%", file=sys.stderr, end="")
    #    signals.append(("broadcaster", "button", 0))
    #    lo, hi = 0, 0
    #    #if i < 4:
    #    #    print("round", i)
    #    while len(signals) > 0:
    #        m, src, v = signals.popleft()
    #        if m == "rx" and v == 0 and presses_before_rx is None:
    #            presses_before_rx = i + 1
    #            print("presses_before_rx", presses_before_rx)
    #        if v == 0:
    #            lo += 1
    #        else:
    #            hi += 1
    #        #if i < 4:
    #        #    print(f"  {src} -{['low','high'][v]}-> {m}")
    #        mod = modules.get(m)
    #        if mod is not None:
    #            r = mod.pulse(src, v)
    #            signals.extend(r)
    #    #if i < 4:
    #    #    print(lo, hi)
    #    lo_total += lo
    #    hi_total += hi
    #    i += 1
    #print("", file=sys.stderr)
    #print(lo_total, hi_total, lo_total*hi_total)
    #print(presses_before_rx)
    #print("")
        
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