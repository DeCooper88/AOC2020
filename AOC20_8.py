from helpers import file_reader
from typing import List, NamedTuple, Union
from copy import copy
import time


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
    def __init__(self, program_lines: List[str]) -> None:
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
    # TODO: not used, change into test
    # t1 = ['nop +0', 'acc +1', 'jmp +4', 'acc +3', 'jmp -3', 'acc -99', 'acc +1', 'nop -4', 'acc +6']

    gc0 = GameConsole(t0)
    assert gc0.first_repeated_line() == 5
    assert gc0.find_wrong_line() == 8

    start_prep = time.perf_counter()
    day8_input = file_reader("inputs/2020_8.txt", output="lines")
    end_prep = time.perf_counter()
    day8 = GameConsole(day8_input)
    p1 = day8.first_repeated_line()
    part_1 = time.perf_counter()
    p2 = day8.find_wrong_line()
    end = time.perf_counter()
    prep_time = round((end_prep - start_prep) * 1000, 1)
    time_p1 = round((part_1 - end_prep) * 1000, 1)
    time_p2 = round((end - part_1) * 1000, 1)
    total_time = round(prep_time + time_p1 + time_p2, 1)
    print(f"Solution part 1: {p1} ({time_p1}ms)")
    print(f"Solution part 2: {p2} ({time_p2}ms)")
    print(f"total runtime including importing and cleaning data: {total_time}ms")
