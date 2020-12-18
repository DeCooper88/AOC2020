from helpers import file_reader
from typing import List, Callable
import math


def regular_math(data: str) -> int:
    """
    Return result of expression using normal math.
    Helper function part 1.
    """
    expression = [int(x) if x not in {'+', '*'} else x for x in data.split(' ')]
    result: int = expression[0]
    operation: str = ""
    for step in expression[1:]:
        if step in {'+', '*'}:
            operation = step
        else:
            calculation = str(result) + operation + str(step)
            result = eval(calculation)
    return result


def funky_math(data: str) -> int:
    """
    Return result of expression using funky math (addition before
    multiplication). Helper function part 2.
    """
    expression = [int(x) if x not in {'+', '*'} else x for x in data.split(' ')]
    for i in range(len(expression)):
        if expression[i] == '+':
            expression[i + 1] += expression[i - 1]
            expression[i - 1] = 1
            expression[i] = 1
        elif expression[i] == '*':
            expression[i] = 1
    return math.prod(expression)


def calculate_expression(original: str, calculator: Callable) -> int:
    """
    Return result of expression. Algorithm will keep stripping out
    parts surrounded by parentheses until there are no more left.
    Then it will return the result of the clean expression.
    Calculator depends on whether it is part 1 or 2.
    """
    if '(' not in original:
        return calculator(original)
    last_open = int
    simplified = original
    while True:
        if '(' not in simplified:
            break
        for i, char in enumerate(simplified):
            if char == '(':
                last_open = i
            elif char == ')':
                start = simplified[:last_open]
                paras = simplified[last_open + 1: i]
                middle = calculator(paras)
                end = simplified[i + 1:]
                simplified = start + str(middle) + end
                break
    return calculator(simplified)


def compute(homework: List[str], calculator: Callable) -> int:
    """
    Evaluate the expression on each line of the homework. Return the sum of
    the resulting values.
    To solve part 1 supply regular_math function as the calculator.
    To solve part 2 supply funky_math function as the calculator.
    """
    result = 0
    for line in homework:
        result += calculate_expression(line, calculator)
    return result


if __name__ == '__main__':
    t0 = "1 + 2 * 3 + 4 * 5 + 6"  # 71, 231
    t1 = "2 * 3 + (4 * 5)"  # 26, 46
    t2 = "5 + (8 * 3 + 9 + 3 * 4 * 3)"  # 437, 1445
    t3 = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"  # 12240, 669060
    t4 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"  # 13632, 23340
    all_tests = [t0, t1, t2, t3, t4]  # 26406, 694122

    assert compute(all_tests, regular_math) == 26406
    assert compute(all_tests, funky_math) == 694122

    day18 = file_reader('inputs/2020_18.txt', output='lines')
    print("solution part 1:", compute(day18, regular_math))
    print("solution part 2:", compute(day18, funky_math))
