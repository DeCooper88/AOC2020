from helpers import file_reader


def get_instruction(data):
    inst, val = data.split(' ')
    return inst, int(val)


def compute(data):
    instructions = [get_instruction(x) for x in data]
    visited = set()
    accumulator = position = 0
    while position not in visited:
        visited.add(position)
        inst, value = instructions[position]
        if inst == 'nop':
            position += 1
        elif inst == 'acc':
            accumulator += value
            position += 1
        elif inst == 'jmp':
            position += value
    return accumulator


def validate_program(instructions):
    final_line = len(instructions) - 1
    visited = set()
    accumulator = position = 0
    while position not in visited:
        visited.add(position)
        inst, value = instructions[position]
        if inst == 'nop':
            position += 1
        elif inst == 'acc':
            accumulator += value
            position += 1
        elif inst == 'jmp':
            position += value
        if position == final_line:
            i, v = instructions[final_line]
            if i == 'acc':
                accumulator += v
            break
    return accumulator if position == final_line else False


def compute_two(data):
    for line, inst in enumerate(data):
        cur_inst = get_instruction(inst)
        instructions = [get_instruction(x) for x in data]
        if cur_inst[0] == 'jmp':
            _, val = cur_inst
            instructions[line] = ('nop', val)
        elif cur_inst[0] == 'nop':
            _, val = cur_inst
            instructions[line] = ('jmp', val)
        outcome = validate_program(instructions)
        if outcome:
            return outcome
    return None


if __name__ == '__main__':
    t0 = ['nop +0', 'acc +1', 'jmp +4', 'acc +3', 'jmp -3', 'acc -99', 'acc +1', 'jmp -4', 'acc +6']
    t1 = ['nop +0', 'acc +1', 'jmp +4', 'acc +3', 'jmp -3', 'acc -99', 'acc +1', 'nop -4', 'acc +6']

    assert compute(t0) == 5
    assert compute_two(t0) == 8

    day8 = file_reader('inputs/2020_8.txt', output='lines')
    print(compute(day8))
    print(compute_two(day8))
