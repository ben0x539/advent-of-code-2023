import os
import re
import typing
from dataclasses import dataclass

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def total(self) -> int:
        return self.x + self.m + self.a + self.s

Check = typing.Callable[[Part], bool]

@dataclass
class Workflow:
    name: str
    rules: list[tuple[Check, str]]
    fallback: str

    def __call__(self, part: Part) -> str:
        for (check, dest) in self.rules:
            if check(part):
                return dest
        return self.fallback

def cmp_op(s: str) -> typing.Callable[[int, int], bool]:
    match s:
        case "<": return lambda a, b: a < b
        case ">": return lambda a, b: a > b
    raise Exception(f"comparison operator isn't < or >: {s}")

def field_op(s: str) -> typing.Callable[[Part], int]:
    match s:
        case "x": return lambda p: p.x
        case "m": return lambda p: p.m
        case "a": return lambda p: p.a
        case "s": return lambda p: p.s
    raise Exception(f"operand isn't x, m, a or s: {s}")

def get_rule(s: str) -> tuple[Check, str]:
    check, _, dest = s.partition(":")
    field, op, val = field_op(check[0]), cmp_op(check[1]), int(check[2:])
    return (lambda part: op(field(part), val), dest)

def get_workflow(s: str) -> Workflow:
    name, _, rules_str = s.partition("{")
    all_rules = rules_str[:-1].split(",")
    rules, fallback = list(map(get_rule, all_rules[:-1])), all_rules[-1]
    return Workflow(name, rules, fallback)

Rule2 = tuple[int, str, int, str]

def get_rule2(s: str) -> Rule2:
    check, _, dest = s.partition(":")
    field, op, val = "xmas".index(check[0]), check[1], int(check[2:])
    return (field, op, val, dest)

Workflow2 = tuple[str, list[Rule2], str]

def get_workflow2(s: str) -> Workflow2:
    name, _, rules_str = s.partition("{")
    all_rules = rules_str[:-1].split(",")
    rules, fallback = list(map(get_rule2, all_rules[:-1])), all_rules[-1]
    return (name, rules, fallback)

def process(workflows: dict[str, Workflow], part: Part) -> bool:
    state = "in"
    while True:
        state = workflows[state](part)
        match state:
            case "A": return True
            case "R": return False

def process2(workflows: dict[str, Workflow2]) -> int:
    accepted = []
    stack = [ ("in", [(1, 4000)] * 4) ]
    while len(stack) > 0:
        state, valid = stack.pop()
        while True:
            if state == "A":
                accepted.append(valid)
                break
            if state == "R":
                break
            _, rules, fallback = workflows[state]
            empty = False
            for (field, op, val, dest) in rules:
                lo, hi = valid[field]
                if op == ">":
                    if hi > val:
                        valid_ = valid[:field] + [(max(val+1, lo), hi)] + valid[field+1:]
                        stack.append((dest, valid_))
                        hi = val
                elif op == "<":
                    if lo < val:
                        valid_ = valid[:field] + [(lo, min(val-1, hi))] + valid[field+1:]
                        stack.append((dest, valid_))
                        lo = val
                if lo > hi:
                    empty = True
                    break
                valid = valid[:field] + [(lo, hi)] + valid[field+1:]
            if empty:
                break
            state = fallback

    #overlap = 0
    #for i, valid in enumerate(accepted):
    #    for valid_ in accepted[:i]:
    #        valid__ = []
    #        v = 1
    #        for field in range(4):
    #            vf, vf_ = valid[field], valid_[field]
    #            lo, hi = max(vf[0], vf_[0]), min(vf[1], vf_[1])
    #            if lo > hi:
    #                break
    #            v *= hi - lo + 1
    #        else:
    #            print(valid, valid_, v)
    #            overlap = v
    #print(overlap)

    total = 0
    for valid in accepted:
        n = 1
        for lo, hi in valid:
            n *= hi-lo+1
        total += n
    return total #- overlap

def run(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        workflows_str, parts_str = list(map(str.split, f.read().split("\n\n")))
    parts = [Part(*map(int, re.findall(r"\d+", part))) for part in parts_str]
    workflows1 = {w.name: w for w in map(get_workflow, workflows_str)}
    print(sum(part.total() for part in parts if process(workflows1, part)))

    workflows2 = {w[0]: w for w in map(get_workflow2, workflows_str)}
    print(process2(workflows2))
    

base, _, today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')
run(f"{base}/inputs/sample-{today}.txt")
run(f"{base}/inputs/input-{today}.txt")