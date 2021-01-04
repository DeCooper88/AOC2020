from typing import Iterable, List, NamedTuple, Union
from copy import copy
from time import perf_counter


def get_input(data_file: str) -> Iterable[str]:
    with open(data_file) as f:
        for line in f.readlines():
            yield line.strip()


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


class GameConsole:
    def __init__(self, program_lines: Iterable[str]) -> None:
        self.lines: List[Instruction] = [get_instruction(x) for x in program_lines]

    def first_repeated_line(self) -> int:
        """
        Return the value accumulator has when the program visits a location
        it had already visited earlier in the program. Is answer day 8 part 1.
        """
        visited = set()
        accumulator = position = 0
        while position not in visited:
            visited.add(position)
            instruction = self.lines[position]
            if instruction.operation == "nop":
                position += 1
            elif instruction.operation == "acc":
                accumulator += instruction.argument
                position += 1
            elif instruction.operation == "jmp":
                position += instruction.argument
        return accumulator

    @staticmethod
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
                final = instructions[final_line]
                if final.operation == "acc":
                    accumulator += final.argument
                break
        return accumulator if position == final_line else False

    def find_wrong_line(self) -> Union[int, bool]:
        """
        Find line for which the Instruction operation needs to be changed. It
        can be changed from 'jmp' to 'nop' or from 'nop' to 'jmp'.
        Fix the line to ensure the program terminates (reaches final line) and
        return the accumulator value. Is answer day 8 part 2.
        """
        for line, instruction in enumerate(self.lines):
            cur_program = copy(self.lines)
            if instruction.operation == "jmp":
                cur_program[line] = Instruction("nop", instruction.argument)
            elif instruction.operation == "nop":
                cur_program[line] = Instruction("jmp", instruction.argument)
            outcome = self.validate_program(cur_program)
            if outcome:
                return outcome
        return False

    def __len__(self):
        return len(self.lines)

    def __repr__(self) -> str:
        program = ""
        for i, line in enumerate(self.lines):
            program += f"Instruction[{i}] -> operation={line.operation}, argument={line.argument}\n"
        return program


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

    gc0 = GameConsole(t0)
    assert gc0.first_repeated_line() == 5
    assert gc0.find_wrong_line() == 8

    start = perf_counter()
    day8_input = get_input("inputs/2020_8.txt")
    sp1 = perf_counter()
    day8 = GameConsole(day8_input)
    p1 = day8.first_repeated_line()
    sp2 = perf_counter()
    p2 = day8.find_wrong_line()
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"Solution part 1: {p1} ({time1}ms)")
    print(f"Solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms\n")
