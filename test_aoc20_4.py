import pytest
import AOC20_4


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
    assert AOC20_4.valid_byr(test_input) == expected


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
    assert AOC20_4.valid_iyr(test_input) == expected


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
    assert AOC20_4.valid_eyr(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('60in', True),
        ('190cm', True),
        ('190in', False),
        ('190', False),
))
def test_valid_hgt(test_input, expected):
    assert AOC20_4.valid_hgt(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('#123abc', True),
        ('#123abz', False),
        ('123abc', False),
        ('#666666', True),
))
def test_valid_hcl(test_input, expected):
    assert AOC20_4.valid_hcl(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('xxx', False),
        ('666', False),
        ('brn', True),
        ('hzl', True),
))
def test_valid_ecl(test_input, expected):
    assert AOC20_4.valid_ecl(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        ('666', False),
        ('a12345678', False),
        ('111111111', True),
        ('123456789', True),
))
def test_valid_pid(test_input, expected):
    assert AOC20_4.valid_pid(test_input) == expected
