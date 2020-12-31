# Advent of code 2020
43/50 :star:

This repo contains my python solutions for [Advent of code 2020](https://adventofcode.com/). Thanks [Eric Wastl](https://twitter.com/ericwastl) for this fun and educational challenge!

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Day 1: [Report Repair](https://adventofcode.com/2020/day/1)
The elves hand you an expense report. For part one you need to find the 2 entries that add up to 2020 and return the product of those. Part two is the same, but for 3 entries.
A simple brute force solution for this problem is nested for loops. However, I used combinations from the itertools module to make it more efficient. During refactoring, I realized it could be made a lot more efficient, by using a set for part one. As set lookups are O(1) you iterate over the set once and for each entry check if 2020 - entry is also in the set. This made the time complexity for this solution linear. Part two could be improved even more. I still use combinations, but of only 2 entries. Then for each combination check if 2020 - sum(combination) is in the set.
Compared to brute force the final solution for part one is 100 times faster and for part two 400 times.