from helpers import file_reader
from typing import List, Dict, Deque
from collections import deque
from pprint import pprint

"""
Kind of a graph. You start at the deepest nested, gou outwards from there and once
you are no longer nested you move to front.
steps: 
    1) find deepest nested. evaluate
    2) find 
    
Create graph with key nesting depth and value index start and end.

Use a stack for opening parentheses. every time you encounter you you add it's index to the stack.

NEW APPROACH:
    1) check if char contains '('
    if not return string
    2) iterate through chars string
    3) keep track of index last seen '('
    4) when first ')' is found:
        a) split string in 3 parts: pre, para, post
        b) calculate value for para
        c) concatenate parts back together.
"""


def nesting_table(data: str) -> Dict:
    parentheses: Deque[int] = deque()
    depth = 0
    nested = {}
    for i, char in enumerate(data):
        if char == '(':
            parentheses.append(i)
            depth += 1
        elif char == ')':
            start = parentheses.pop()
            nested[(depth, start)] = (start + 1, i)
            depth -= 1
    return nested


def extract_value(para_pos: int, expr: str):
    pass


def expression_list(data: str) -> List[str]:
    data = data.replace(')', ' )')
    data = data.replace('(', '( ')
    return data.split(' ')


def parentheses_values(expression: str) -> Dict:
    print(expression)
    nested = nesting_table(expression)
    paras = sorted(nested.keys(), reverse=True)
    para_table = {}
    for par in paras:
        start, end = nested[par]
        exp = expression[start: end]
        print(par, '->', exp)
        par_positions = deque([par[1] + i for i, p in enumerate(exp, start=1) if p == '('])
        print(par_positions)
        # exp = exp.replace(')', ' )')
        # exp = exp.replace('(', '( ')
        exp_list = expression_list(exp)
        print(exp_list)
        result = 0
        operation = ""
        inside_parantheses = 0
        # for char in exp_list:
        #     if char == ')':
        #         inside_parantheses -= 1
        #         continue
        #     elif inside_parantheses:
        #         continue
        #     if char in {'+', '*'}:
        #         operation = char
        #     elif char == '(':
        #
        # #
        # #
        # # if
    return paras


def calculate(input: str) -> int:
    expression = [int(x) if x not in {'+', '*'} else x for x in input.split(' ')]
    result: int = expression[0]
    operation: str = ""
    for step in expression[1:]:
        if step in {'+', '*'}:
            operation = step
        else:
            calculation = str(result) + operation + str(step)
            # print(calculation)
            result = eval(calculation)
    # print(expression)
    return result


def calculate_expression(original):
    # print("original", original)
    if '(' not in original:
        return calculate(original)
    last_open = int
    start = paras = end = ""
    simplified = original
    while True:
        # print("simplified", simplified)
        if '(' not in simplified:
            break
            # return simplified
        for i, char in enumerate(simplified):
            if char == '(':
                last_open = i
            elif char == ')':
                start = simplified[:last_open]
                paras = simplified[last_open + 1: i]
                # print("stripped", paras)
                middle = calculate(paras)
                end = simplified[i + 1:]
                simplified = start + str(middle) + end
                break
    # print(simplified)
    return calculate(simplified)


def compute(data):
    result = 0
    for line in data:
        # print(line)
        result += calculate_expression(line)
    return result


# answers = 71, 26, 437, 12240, 13632

t0 = "1 + 2 * 3 + 4 * 5 + 6"  # 71
t1 = "2 * 3 + (4 * 5)"  # 26
t2 = "5 + (8 * 3 + 9 + 3 * 4 * 3)"  # 437
t3 = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"  # 12240
t4 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"  # 13632
all_tests = [t0, t1, t2, t3, t4]  # 26406

assert calculate(t0) == 71
assert compute(all_tests) == 26406

day18 = file_reader('inputs/2020_18.py', output='lines')
print("solution part 1:", compute(day18))
