from collections import deque, Counter
from helpers import file_reader
from typing import Dict, List, Set
from copy import copy
from pprint import pprint

"""
Plan:
1) Create a dictionary that maps children to parents.
2) create message_table variable (=dict) that will hold messages for
   each rule (message = rule translated to 'a'/'b' sequences).
2) create frontier variable (=deque) that holds unprocessed parents
3) find keys for a and b.
4) add keys a and b to frontier
start while loop
    a) pop rule from left frontier.
    b) check if all it's children are in message_table
        if not --> append rule frontier (so ends up at end of line)
    c) start processing rules
        if rule already in message_table --> continue
    
"""

# TODO: Got stuck. Idea: make a new test and try to get it working on that
# TODO: The problem seems to occur with rules of len 1 (42, 8 etc).


def rules_table(rule_strings):
    rule_strings = [rule.strip() for rule in rule_strings.strip().split('\n')]
    rules = {}
    for rule in rule_strings:
        k, v = rule.split(': ')
        if v[1] in {"a", "b"}:
            rules[int(k)] = v[1]
        else:
            possibilities = v.split(' | ')
            children = []
            for child in possibilities:
                options = [int(x) for x in child.split(' ')]
                children.append(tuple(options))
            rules[int(k)] = children
    return rules


class Image:
    def __init__(self, data: str) -> None:
        raw_rules, raw_messages = data.split('\n\n')
        self.rules: Dict = rules_table(raw_rules)
        self.messages: List[str] = [m.strip() for m in raw_messages.strip().split('\n')]

    @property
    def parents(self):
        """Return graph that maps rule to all it's parents."""
        all_parents = {}
        for mom, kids in self.rules.items():
            unique = set()
            for kid in kids:
                for k in kid:
                    unique.add(k)
            for un in unique:
                if un not in all_parents:
                    all_parents[un] = [mom]
                else:
                    all_parents[un].append(mom)
        return all_parents

    def get_children(self, current_rule) -> Set:
        """Return a set with all rules that this rule depends on."""
        dependencies = set()
        rules = self.rules[current_rule]
        for rule in rules:
            for r in rule:
                dependencies.add(r)
        return dependencies

    def rule_strings(self):
        message_table = {}
        start_a = self.parents['a'][0]
        start_b = self.parents['b'][0]
        message_table[start_a] = ['a']
        message_table[start_b] = ['b']
        starters = set(self.parents[start_a]) | set(self.parents[start_b])
        # print("starters", starters)
        frontier = deque()
        # populate frontier with parents of 'a' and 'b'
        frontier.extend(starters)
        while frontier:
            # print("frontier", len(frontier))
            # print("set(frontier)", len(set(frontier)))
            # print(frontier)
            current_rule = frontier.popleft()
            # get all rules that need to be present to process current rule
            needs = self.get_children(current_rule)
            all_present = True
            # check if all requirements are present
            for req in needs:
                if req not in message_table:
                    all_present = False
                    # frontier.append(current_rule)
                    break
            # if not all required rules are present append current_rule back onto frontier
            if not all_present:
                # TODO: BUG, rules end up in frontier multiple times. Needs fix!!
                frontier.append(current_rule)
                continue
            # add parents current rule to frontier except if current_rule == 0
            if current_rule != 0:  # WARNING: starter node hard-coded
                parents = self.parents[current_rule]
                for parent in parents:
                    if parent not in message_table:
                        frontier.append(parent)
            # update message table
            messages = []
            for rule in self.rules[current_rule]:
                # print("rule:", rule)
                sub_msg = ""
                if len(rule) == 1:
                    k = rule[0]
                    # print("current_rule:", current_rule, "rule:", k)
                    v = message_table[k]
                    # print("v", v)
                    message_table[current_rule] = copy(v)
                    # print(f"message_table[{current_rule}]", message_table[current_rule])
                    continue
                subs_a = message_table[rule[0]]
                subs_b = message_table[rule[1]]
                # print("subs_a:", subs_a)
                # print("subs_b", subs_b)
                for a in subs_a:
                    for b in subs_b:
                        # print("a=", a, "b=", b)
                        msg = a + b
                        # print(msg)
                        messages.append(msg)
            message_table[current_rule] = messages
        return message_table


t0_raw = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

t1_raw = """
0: 4 1
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

# t0 = Image(t0_raw)
# print(t0.rules)
# print(t0.messages)
# print(t0.parents)
# assert t0.get_children(0) == {1, 4, 5}
# assert t0.get_children(1) == {2, 3}
# assert t0.get_children(2) == {4, 5}
# assert t0.get_children(3) == {4, 5}
# assert t0.get_children(4) == {'a'}
# assert t0.get_children(5) == {'b'}

t1 = Image(t1_raw)
# print(t1.rules)
# print(t1.messages)
# print(t1.parents)
# pprint(t1.rule_strings())
# print()

day19_raw = file_reader('inputs/2020_19.txt')
day19 = Image(day19_raw)
pprint(day19.messages)
pprint(day19.rules)
# print(day19.rule_strings())
# print(day19.rule_strings()[20])
# print(day19.rule_strings()[30])
# print(day19.rule_strings()[5])
# print(day19.rule_strings()[22])
# print(day19.rule_strings()[43])
# print(day19.rule_strings()[53])
# print(day19.rule_strings()[65])
# print()


rule_42 = day19.rule_strings()[42]
rule_11 = day19.rule_strings()[11]
print(len(rule_42))
print(len(rule_11))
print(len(rule_42[0]))
print(len(rule_11[0]))
rule_0 = set()
for i, a in enumerate(rule_42):
    for b in rule_11:
        rule_0.add(a + b)
# print(rule_42)
# print(rule_11[0])
# print(len(rule_0))
# print(len(day19.messages))

# pprint(rule_0)

# checker = set(rule_42)
# counter = 0
# potentials = []
# for msg in day19.messages:
#     first_8 = msg[:8]
#     # print(first_8)
#     if first_8 in checker:
#         potentials.append(msg)
#         counter += 1
# print()
# print(counter)
# pprint(potentials)
#
# len_table = Counter()
# for p in potentials:
#     len_msg = len(p)
#     len_table[len_msg] += 1
# print(len_table)
