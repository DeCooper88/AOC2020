from helpers import file_reader
from typing import List, Optional, Tuple, Union
from itertools import product
from time import perf_counter


def get_info(data: List[str]) -> List:
    # TODO: refactor to optimize for use with part 1 and part 2
    # currently it converts val to binary, but for part 2 need int
    clean: List[Tuple[Union[int, str], str]] = []
    for line in data:
        if line.startswith('mask'):
            _, m = line.strip().split(' = ')
            clean.append(('mask', m))
        elif line.startswith('mem'):
            n, val = line.strip().split(' = ')
            name = n[3:]
            name = name.replace('[', '')
            name = name.replace(']', '')
            clean.append((int(name), bin(int(val))))
    return clean


def convert_binary(mask: Optional[str], bin_num: str) -> int:
    """
    Apply mask to binary number and convert to int.
    Helper function part 1.
    """
    good_bits = bin_num[2:]
    pad_number = 36 - len(good_bits)
    pad_string = pad_number * '0'
    binary = pad_string + good_bits
    new_binary = []
    for i, val in enumerate(mask):
        if val == 'X':
            new_binary.append(binary[i])
        else:
            new_binary.append(val)
    return int("".join(new_binary), 2)


def compute(data: List[str]) -> int:
    """Return answer day 14 part 1."""
    instructions = get_info(data)
    valid_nums = {}
    mask: Optional[str] = None
    for line in instructions:
        if line[0] == 'mask':
            mask = line[1]
        else:
            address, num = line
            valid_nums[address] = convert_binary(mask, num)
    return sum(valid_nums.values())


def address_combos(original: str, float_locs: List[int]) -> List[int]:
    # TODO: refactor to generator
    """Return all possible addresses"""
    combos = product((0, 1), repeat=len(float_locs))
    addresses = []
    for combo in combos:
        address = list(original)
        for i, float in enumerate(float_locs):
            address[float] = str(combo[i])
        ad = "".join(address)
        addresses.append(int(ad, 2))
    return addresses


def get_addresses(mask: str, number: int) -> List[int]:
    # TODO: can perhaps be changed into generator function
    original = bin(number)[2:]
    shortage = 36 - len(original)
    address = list(shortage * '0' + original)
    floating_bits = []
    for i, val in enumerate(mask):
        if val == '1':
            address[i] = '1'
        elif val == 'X':
            floating_bits.append(i)
            address[i] = 'X'
    new_address = "".join(address)
    # TODO: refactor: cooperation with address_combo function can be simplified/improved
    all_addresses = address_combos(new_address, floating_bits)
    return all_addresses


def compute_two(data: List[str]) -> int:
    """Return answer day 14 part 2."""
    instructions = get_info(data)
    valid_nums = {}
    mask = str
    for line in instructions:
        if line[0] == 'mask':
            mask = line[1]
        else:
            val = int(line[1], 2)
            adds = get_addresses(mask, line[0])
            for add in adds:
                valid_nums[add] = val
    return sum(valid_nums.values())


t0_raw = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

t1_raw = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

t0 = [line.strip() for line in t0_raw.strip().split('\n')]
t1 = [line.strip() for line in t1_raw.strip().split('\n')]

assert convert_binary('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', '0b1011') == 73
assert convert_binary('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', '0b1100101') == 101
assert convert_binary('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', '0b0') == 64

assert address_combos('000000000000000000000000000000X1101X', [30, 35]) == [26, 27, 58, 59]
assert address_combos('00000000000000000000000000000001101X', [35]) == [26, 27]

assert get_addresses('000000000000000000000000000000X1001X', 42) == [26, 27, 58, 59]
assert get_addresses('00000000000000000000000000000000X0XX', 26) == [16, 17, 18, 19, 24, 25, 26, 27]

assert compute(t0) == 165
assert compute_two(t1) == 208

st = perf_counter()
day14 = file_reader('inputs/2020_14.txt', output='lines')
st_p1 = perf_counter()
p1 = compute(day14)
st_p2 = perf_counter()
p2 = compute_two(day14)
end = perf_counter()
time_p1 = round((st_p2 - st_p1) * 1000, 1)
time_p2 = round((end - st_p2) * 1000, 1)
total_time = round((end - st) * 1000, 1)
print(f"solution part 1: {p1} ({time_p1}ms)")
print(f"solution part 2: {p2} ({time_p2}ms)")
print(f"total execution time: {total_time}ms")
