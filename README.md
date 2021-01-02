# Advent of code 2020
#### 43/50 :star:

This repo contains my python solutions for [Advent of code 2020](https://adventofcode.com/). Thanks [Eric Wastl](https://twitter.com/ericwastl) for this fun and educational challenge! Days for which I wrote notes in the readme have been refactored. The code for other days may still be messy.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Day 1: [Report Repair](https://adventofcode.com/2020/day/1)
The elves hand you an expense report. For part one you need to find the 2 entries that add up to 2020 and calculate the product of those. Part two is the same, but for 3 entries.
A simple brute force solution for this problem is nested for loops. However, I used combinations [(n choose k)](https://en.wikipedia.org/wiki/Binomial_coefficient) from the itertools module to make it more efficient. During refactoring, I realized using a set would be more efficient. As set lookups are O(1) you iterate over the set once and for each entry check if 2020 - entry is also in the set. This makes the time complexity for part one linear. Part two could be improved even more. I still use combinations, but of only 2 entries. Then for each combination check if 2020 - sum(combination) is in the set.
Compared to brute force the final solution for part one is 100 times faster and for part two 400 times.

*(total runtime: 1.6ms)*

### Day 2: [Password Philosophy](https://adventofcode.com/2020/day/2)
The Toboggan rental office needs you to do password validation for them. You are given a list of strings, where each line contains a password and the policy it needs to comply with.
First I converted the password-policy strings into namedtuples. After that the rest of the problem is straightforward.
Initially I used a separate function for the validation of part two, but by using exclusive or (XOR) I was able to get rid of that. This made the code more readable and also slightly faster. Part two policy indexes from 1, so the function needs to account for that.

*(total runtime: 4.25ms)*

### Day 3: [Toboggan Trajectory](https://adventofcode.com/2020/day/3)
You take a toboggan (sled) to the airport, but steering is hard. You receive tree coordinates and need to calculate how many trees you are likely to hit on a given trajectory. The map you receive is incomplete. If you go off the map on the Eastern edge before reaching the Southern edge you need to revert to the Western edge. This can be achieved by applying modulo to the column (EAST-WEST) parameter of the grid.
Only one function is needed for both parts, as the trajectories parameter is a list. For part one there is 1 trajectory and for part two there are 5.

*(total runtime: 0.49ms)*

### Day 4: [Passport Processing](https://adventofcode.com/2020/day/4)
On day four you arrive at the airport and end up in a very long line for the passport scanners. You can speed up your progress by helping out with passport validation.
The function for part one converts the strings with passport data to a dictionary. If this dictionary contains all the required fields it is added to a list. This list is the input for part two. The answer for part one is the length of this list.
For part two I used TDD (Test Driven Development) with pytest. For every validation (hair color, height etc) I wrote a separate function that could be tested. All 7 validation functions are then applied to every passport. Only passports for which all 7 validations return True are counted.

*(total runtime: 2.07ms)*

### Day 5: [Binary Boarding](https://adventofcode.com/2020/day/5)
When you board the plane you discover that you dropped your boarding pass. Based on nearby boarding passes you attempt to discover your seat.
The problem description immediately led me down the binary search path. This worked fine. After finding the solution, I discovered that the boarding pass string is actually a binary number, where Bs and Rs are ones and Fs and Ls are zeros. Hand smacks head! That would have made solving it a lot easier. Converting binary to int is very easy in python. Just add 2 (binary is base 2) as second parameter to the int function.

*(total runtime: 1.6ms)*