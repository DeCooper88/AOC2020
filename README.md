# Advent of code 2020
#### 43/50 :star:

This repo contains my python solutions for [Advent of code 2020](https://adventofcode.com/). Thanks [Eric Wastl](https://twitter.com/ericwastl) for this fun and educational challenge!

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Day 1: [Report Repair](https://adventofcode.com/2020/day/1)
The elves hand you an expense report. For part one you need to find the 2 entries that add up to 2020 and calculate the product of those. Part two is the same, but for 3 entries.
A simple brute force solution for this problem is nested for loops. However, I used combinations from the itertools module to make it more efficient. During refactoring, I realized it could be made a lot more efficient, by using a set. As set lookups are O(1) you iterate over the set once and for each entry check if 2020 - entry is also in the set. This made the time complexity for this solution linear. Part two could be improved even more. I still use combinations, but of only 2 entries. Then for each combination check if 2020 - sum(combination) is in the set.
Compared to brute force the final solution for part one is 100 times faster and for part two 400 times.

*(total runtime: 1.6ms)*

### Day 2: [Password Philosophy](https://adventofcode.com/2020/day/2)
The Toboggan rental office needs you to do password validation for them. You are given a list of strings, where each line contains a password and the policy it needs to comply with.
First I converted the password-policy strings into namedtuples. After that the rest of the problem is straightforward.
Initially used a separate function for the validation of part two, but by using exclusive or (XOR) I was able to get rid of that. This made the code more readable and also slightly faster. Part two policy uses 1-indexing, so function needs to account for that.

*(total runtime: 4.25ms)*
