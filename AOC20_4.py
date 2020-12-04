from helpers import file_reader
import time


def passport_dict(passport_string):
    """Convert password string into a dictionary."""
    data_fields = passport_string.split(' ')
    pp_dict = {}
    for line in data_fields:
        k, v = line.split(':')
        pp_dict[k] = v
    return pp_dict


def contains_all_fields(passport_string):
    """Return True if password contains all the required fields."""
    pw_dict = passport_dict(passport_string)
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    for field in required_fields:
        if field not in pw_dict:
            return False
    return True


def valid_byr(data):
    """byr (Birth Year) - four digits; at least 1920 and at most 2002."""
    if not data.isdigit():
        return False
    return 1920 <= int(data) <= 2002


def valid_iyr(data):
    """iyr (Issue Year) - four digits; at least 2010 and at most 2020."""
    if not data.isdigit():
        return False
    return 2010 <= int(data) <= 2020


def valid_eyr(data):
    """eyr (Expiration Year) - four digits; at least 2020 and at most 2030."""
    if not data.isdigit():
        return False
    return 2020 <= int(data) <= 2030


def valid_hgt(data):
    """
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    """
    metric = data[-2:]
    if metric not in {'in', 'cm'}:
        return False
    number = int(data[:len(data) - 2])
    if metric == "cm" and 150 <= number <= 193:
        return True
    if metric == 'in' and 59 <= number <= 76:
        return True
    return False


def valid_hcl(data):
    """hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f."""
    if len(data) != 7:
        return False
    if data[0] != '#':
        return False
    valid_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}
    for char in data[1:]:
        if char not in valid_chars:
            return False
    return True


def valid_ecl(data):
    """ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth."""
    valid_eye_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    return data in valid_eye_colors


def valid_pid(data):
    """pid (Passport ID) - a nine-digit number, including leading zeroes."""
    return len(data) == 9 and data.isdigit()


def validate_passport(pw_data):
    pw_details = passport_dict(pw_data)
    validators = {'byr': valid_byr,
                  'iyr': valid_iyr,
                  'eyr': valid_eyr,
                  'hgt': valid_hgt,
                  'hcl': valid_hcl,
                  'ecl': valid_ecl,
                  'pid': valid_pid
                  }
    valid_fields = {}
    # TODO: refactor, overkill and dodgy as hell
    for key, checker in validators.items():
        test_input = pw_details[key]
        valid_fields[key] = checker(test_input)
    all_checks = valid_fields.values()
    return False not in all_checks


def pre_filter(passports, return_count=False):
    valid_passports = []
    for line in passports:
        if contains_all_fields(line):
            valid_passports.append(line)
    return len(valid_passports) if return_count else valid_passports


def compute(data):
    # TODO: remove after all refactors done
    valid = 0
    for pw in data:
        if contains_all_fields(pw):
            valid += 1
    return valid


def compute_two(data):
    # TODO: Remove below line as repeats work done for part one.
    filtered_pw = pre_filter(data)
    valid = 0
    for pw in filtered_pw:
        if validate_passport(pw):
            valid += 1
    return valid


if __name__ == '__main__':
    # TODO: improve timing
    start_prep = time.perf_counter()
    # TODO: refactor all asserts into tests
    t0 = 'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm'
    t1 = 'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929'
    t2 = 'hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm'
    t3 = 'hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in'
    p1_tests = [t0, t1, t2, t3]
    assert compute(p1_tests) == 2

    # p2 tests - false:
    pc0 = "eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926"
    pc1 = "iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946"
    pc2 = "hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277"
    pc3 = "hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007"
    assert validate_passport(pc0) == False
    assert validate_passport(pc1) == False
    assert validate_passport(pc2) == False
    assert validate_passport(pc3) == False

    # p2 tests - true
    pc4 = "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"
    pc5 = "eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"
    pc6 = "hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022"
    pc7 = "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"
    assert validate_passport(pc4) == True
    assert validate_passport(pc5) == True
    assert validate_passport(pc6) == True
    assert validate_passport(pc7) == True

    p2_tests = [pc0, pc1, pc2, pc3, pc4, pc5, pc6, pc7]

    assert compute_two(p1_tests) == 2
    assert compute_two(p2_tests) == 4

    day4_raw = file_reader('inputs/2020_4.txt')
    day4_b = day4_raw.replace('\n\n', ';')
    day4_c = day4_b.split(';')
    day4 = [x.replace('\n', ' ') for x in day4_c]
    end_prep = time.perf_counter()
    # TODO: use pre_filer instead of compute function
    # TODO: then use len to compute answer for part one
    p1 = compute(day4)
    part_1 = time.perf_counter()
    p2 = compute_two(day4)
    end = time.perf_counter()
    print(p1)
    print(p2)
    print("prep stuff:", (end_prep - start_prep) * 1000)
    print("part 1:", (part_1 - end_prep) * 1000)
    print("part 2:", (end - part_1) * 1000)
