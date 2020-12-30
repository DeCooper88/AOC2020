import pytest
import AOC20_04

t0 = 'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm'
t1 = 'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929'
t2 = 'hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm'
t3 = 'hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in'
p1_tests = [t0, t1, t2, t3]
p1_filtered = AOC20_04.compute_p1(p1_tests)

pc0 = "eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926"
pc1 = "iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946"
pc2 = "hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277"
pc3 = "hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007"
pc4 = "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"
pc5 = "eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"
pc6 = "hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022"
pc7 = "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"
p2_tests = [pc0, pc1, pc2, pc3, pc4, pc5, pc6, pc7]


@pytest.mark.parametrize('test_input, expected', (
        (pc0, False),
        (pc1, False),
        (pc2, False),
        (pc3, False),
        (pc4, True),
        (pc5, True),
        (pc6, True),
        (pc7, True),
))
def test_validate_passport(test_input, expected):
    assert AOC20_04.validate_passport(test_input) == expected


def test_compute_p1():
    assert len(AOC20_04.compute_p1(p1_tests)) == 2


@pytest.mark.parametrize('test_input, expected', (
        ('a302', False),
        ('1', False),
        ('1900', False),
        ('1920', True),
        ('2000', True),
        ('2002', True),
        ('2010', False),
        ('2020', False),
        ('2050', False),
        ('66666', False),
))
def test_valid_byr(test_input, expected):
    """byr (Birth Year) - four digits; at least 1920 and at most 2002."""
    assert AOC20_04.valid_byr(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('a302', False),
        ('1', False),
        ('1900', False),
        ('1920', False),
        ('2000', False),
        ('2002', False),
        ('2010', True),
        ('2020', True),
        ('2050', False),
        ('66666', False),
))
def test_valid_iyr(test_input, expected):
    """iyr (Issue Year) - four digits; at least 2010 and at most 2020."""
    assert AOC20_04.valid_iyr(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('a302', False),
        ('1', False),
        ('1900', False),
        ('1920', False),
        ('2000', False),
        ('2020', True),
        ('2025', True),
        ('2030', True),
        ('2050', False),
        ('66666', False),
))
def test_valid_eyr(test_input, expected):
    """eyr (Expiration Year) - four digits; at least 2020 and at most 2030."""
    assert AOC20_04.valid_eyr(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('60in', True),
        ('190cm', True),
        ('190in', False),
        ('190', False),
))
def test_valid_hgt(test_input, expected):
    assert AOC20_04.valid_hgt(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('#123abc', True),
        ('#123abz', False),
        ('123abc', False),
        ('#666666', True),
))
def test_valid_hcl(test_input, expected):
    assert AOC20_04.valid_hcl(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('xxx', False),
        ('666', False),
        ('brn', True),
        ('hzl', True),
))
def test_valid_ecl(test_input, expected):
    assert AOC20_04.valid_ecl(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('666', False),
        ('a12345678', False),
        ('111111111', True),
        ('123456789', True),
))
def test_valid_pid(test_input, expected):
    assert AOC20_04.valid_pid(test_input) == expected


def test_compute_two_p1():
    assert AOC20_04.compute_p2(p1_filtered) == 2


def test_compute_two_p2():
    assert AOC20_04.compute_p2(p2_tests) == 4
