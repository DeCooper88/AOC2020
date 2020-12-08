from helpers import file_reader
from typing import List, NamedTuple, Union


class Instruction(NamedTuple):
    """
    Instruction line for GameConsole. Operations:
        acc -> increase/decrease accumulator by value in argument
               move to next position (position += 1)
        jmp -> jump to new position. new position -> position += argument
        nop -> do nothing
               move the next position (position += 1)
    """

    operation: str
    argument: int


def get_instruction(data: str) -> Instruction:
    """Return instruction string as Instruction namedtuple"""
    op, arg = data.split(" ")
    return Instruction(op, int(arg))


def compute(data: List[str]) -> int:
    """
    Return the value accumulator has when the program visits a location
    it had already visited earlier in the program. Is answer part 1.
    """
    instructions = [get_instruction(x) for x in data]
    visited = set()
    accumulator = position = 0
    while position not in visited:
        visited.add(position)
        instruction = instructions[position]
        if instruction.operation == "nop":
            position += 1
        elif instruction.operation == "acc":
            accumulator += instruction.argument
            position += 1
        elif instruction.operation == "jmp":
            position += instruction.argument
    return accumulator


def validate_program(instructions: List[Instruction]) -> Union[int, bool]:
    """
    Return accumulator value if the program reaches it's last line,
    else return False.
    """
    final_line = len(instructions) - 1
    visited = set()
    accumulator = position = 0
    while position not in visited:
        visited.add(position)
        instruction = instructions[position]
        if instruction.operation == "nop":
            position += 1
        elif instruction.operation == "acc":
            accumulator += instruction.argument
            position += 1
        elif instruction.operation == "jmp":
            position += instruction.argument
        if position == final_line:
            i, v = instructions[final_line]
            if i == "acc":
                accumulator += v
            break
    return accumulator if position == final_line else False


def compute_two(data: List[str]) -> Union[int, bool]:
    """
    Find line for which the Instruction operation needs to be changed. It
    can be changed from 'jmp' to 'nop' or from 'nop' to 'jmp'.
    Fix the line to ensure the program terminates (reaches final line) and
    return the accumulator value.
    """
    for line, inst in enumerate(data):
        cur_instruction = get_instruction(inst)
        instructions = [get_instruction(x) for x in data]
        if cur_instruction.operation == "jmp":
            instructions[line] = Instruction("nop", cur_instruction.argument)
        elif cur_instruction.operation == "nop":
            instructions[line] = Instruction("jmp", cur_instruction.argument)
        outcome = validate_program(instructions)
        if outcome:
            return outcome
    return False


if __name__ == "__main__":
    t0 = [
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6",
    ]
    # TODO: not used, change into test
    # t1 = ['nop +0', 'acc +1', 'jmp +4', 'acc +3', 'jmp -3', 'acc -99', 'acc +1', 'nop -4', 'acc +6']

    assert compute(t0) == 5
    assert compute_two(t0) == 8

    day8 = file_reader("inputs/2020_8.txt", output="lines")
    print(compute(day8))
    print(compute_two(day8))
