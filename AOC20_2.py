from helpers import file_reader, translator
from collections import Counter, namedtuple

Password = namedtuple("Password", "mini maxi char content")


def translate_pw(pw_string):
    mapper = {'-': ',', ' ': ',', ':': ''}
    a = translator(pw_string, mapper)
    mi, ma, ch, name = a.split(',')
    cur_pw = Password(int(mi) - 1, int(ma) - 1, ch, name)
    return cur_pw


def valid_pw(password):
    valid = 0
    for pos in (password.mini, password.maxi):
        if pos >= len(password.content):
            continue
        if password.content[pos] == password.char:
            valid += 1
    return valid == 1


def compute(data):
    mapper = {'-': ',', ' ': ',', ':': ''}
    valid = 0
    for pw in data:
        cpw = translator(pw, mapper)
        mini, maxi, char, password = cpw.split(',')
        char_count = Counter(password)
        if int(mini) <= char_count[char] <= int(maxi):
            valid += 1
    return valid


def compute_two(data):
    valid = 0
    for pw in data:
        password = translate_pw(pw)
        if valid_pw(password):
            valid += 1
    return valid


if __name__ == '__main__':
    t0 = '1-3 a: abcde'
    t1 = '1-3 b: cdefg'
    t2 = '2-9 c: ccccccccc'
    test_cases = [t0, t1, t2]

    assert compute(test_cases) == 2
    assert compute_two(test_cases) == 1

    day2 = file_reader('2020_2', output='lines')
    print(compute(day2))
    print(compute_two(day2))
