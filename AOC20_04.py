from typing import Dict, Iterable, List
from time import perf_counter


def get_input(data_file: str) -> Iterable[str]:
    """Import data and yield passport data."""
    with open(data_file) as f:
        return (x.replace("\n", " ") for x in f.read().strip().split("\n\n"))


def passport_dict(passport: str) -> Dict[str, str]:
    """Convert passport string into a dictionary."""
    data_fields = passport.split(" ")
    pp_dict = {}
    for line in data_fields:
        k, v = line.split(":")
        pp_dict[k] = v
    return pp_dict


def contains_all_fields(passport: str) -> bool:
    """Return True if passport contains all the required fields."""
    pw_dict = passport_dict(passport)
    required_fields = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
    for field in required_fields:
        if field not in pw_dict:
            return False
    return True


def valid_byr(data: str) -> bool:
    """byr (Birth Year) - four digits; at least 1920 and at most 2002."""
    if not data.isdigit():
        return False
    return 1920 <= int(data) <= 2002


def valid_iyr(data: str) -> bool:
    """iyr (Issue Year) - four digits; at least 2010 and at most 2020."""
    if not data.isdigit():
        return False
    return 2010 <= int(data) <= 2020


def valid_eyr(data: str) -> bool:
    """eyr (Expiration Year) - four digits; at least 2020 and at most 2030."""
    if not data.isdigit():
        return False
    return 2020 <= int(data) <= 2030


def valid_hgt(data: str) -> bool:
    """
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    """
    metric = data[-2:]
    if metric not in {"in", "cm"}:
        return False
    number = int(data[: len(data) - 2])
    if metric == "cm" and 150 <= number <= 193:
        return True
    if metric == "in" and 59 <= number <= 76:
        return True
    return False


VALID_HAIRCOLOUR_CHARS = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
}


def valid_hcl(data: str) -> bool:
    """hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f."""
    if len(data) != 7:
        return False
    if data[0] != "#":
        return False
    for char in data[1:]:
        if char not in VALID_HAIRCOLOUR_CHARS:
            return False
    return True


def valid_ecl(data: str) -> bool:
    """ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth."""
    valid_eye_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    return data in valid_eye_colors


def valid_pid(data: str) -> bool:
    """pid (Passport ID) - a nine-digit number, including leading zeroes."""
    return len(data) == 9 and data.isdigit()


def validate_passport(passport: str) -> bool:
    """Return True if all fields of passport contain valid data."""
    passport_data = passport_dict(passport)
    validators = {
        "byr": valid_byr,
        "iyr": valid_iyr,
        "eyr": valid_eyr,
        "hgt": valid_hgt,
        "hcl": valid_hcl,
        "ecl": valid_ecl,
        "pid": valid_pid,
    }
    for passport_field, validation_function in validators.items():
        test_input = passport_data[passport_field]
        if not validation_function(test_input):
            return False
    return True


def compute_p1(passport_data: Iterable[str]) -> List[str]:
    """
    Return list of passports that contain all valid fields. Number of
    valid passports in list is answer fro part one. List itself is input
    for part two.
    """
    valid_passports = []
    for line in passport_data:
        if contains_all_fields(line):
            valid_passports.append(line)
    return valid_passports


def compute_p2(data: List[str]) -> int:
    """Return number of valid passports. Solution part two."""
    valid = 0
    for pw in data:
        if validate_passport(pw):
            valid += 1
    return valid


if __name__ == "__main__":
    start = perf_counter()
    day4 = get_input("inputs/2020_4.txt")
    sp1 = perf_counter()
    all_valid_passports = compute_p1(day4)
    p1 = len(all_valid_passports)
    sp2 = perf_counter()
    p2 = compute_p2(all_valid_passports)
    end = perf_counter()

    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"Solution part 1: {p1} ({time1}ms)")
    print(f"Solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms\n")
