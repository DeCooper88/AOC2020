from helpers import file_reader, translator
from collections import namedtuple
from time import perf_counter

Password = namedtuple("Password", "low high char content")


def translate_password(pw_string):
    """Convert string to namedtuple: Password"""
    mapper = {'-': ',', ' ': ',', ':': ''}
    clean_pw_string = translator(pw_string, mapper)
    mi, ma, ch, name = clean_pw_string.split(',')
    return Password(int(mi), int(ma), ch, name)


def contains_one(password):
    """
    Return True if password contains correct character
    in only one of the two given position.
    """
    valid = 0
    for position in (password.low, password.high):
        # reduce position by one to account for 0-indexing
        if password.content[position - 1] == password.char:
            valid += 1
    return valid == 1


def compute_one(data):
    """Return answer part 1 of AoC day 2"""
    valid = 0
    for line in data:
        password = translate_password(line)
        char_count = password.content.count(password.char)
        if password.low <= char_count <= password.high:
            valid += 1
    return valid


def compute_two(data):
    """Return answer part 2 of AoC day 2"""
    valid = 0
    for line in data:
        password = translate_password(line)
        if contains_one(password):
            valid += 1
    return valid


if __name__ == '__main__':
    t0 = '1-3 a: abcde'  # True, True
    t1 = '1-3 b: cdefg'  # False, False
    t2 = '2-9 c: ccccccccc'  # True, False
    t3 = '7-15 w: wwwwwcqwwwwwwwww'  # True, True
    t4 = '13-14 s: wznksvkfvfskfs'  # False, True

    test_cases = [t0, t1, t2, t3, t4]

    assert compute_one(test_cases) == 3
    assert compute_two(test_cases) == 3

    day2 = file_reader('2020_2', output='lines')

    start = perf_counter()
    p1 = compute_one(day2)
    middle = perf_counter()
    p2 = compute_two(day2)
    end = perf_counter()
    t1 = int((middle - start) * 1000)
    t2 = int((end - middle) * 1000)
    print(f"solution part 1: {p1} ({t1}ms)")
    print(f"solution part 2: {p2} ({t2}ms)")
