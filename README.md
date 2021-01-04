# Advent of code 2020
#### 43/50 :star:

This repo contains my python solutions for [Advent of code 2020](https://adventofcode.com/). Thanks [Eric Wastl](https://twitter.com/ericwastl) for this fun and educational challenge! Days for which I wrote notes in the readme have been refactored. The code for other days may still be messy. The runtimes are a rough non-scientific estimate based on 5 runs.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Day 1: [Report Repair](https://adventofcode.com/2020/day/1)
The elves hand you an expense report. For part one you need to find the 2 entries that add up to 2020 and calculate the product of those. Part two is the same, but for 3 entries.<br>
A simple brute force solution for this problem is nested for loops. However, I used combinations [(n choose k)](https://en.wikipedia.org/wiki/Binomial_coefficient) from the itertools module to make it more efficient. During refactoring, I realized using a set would be more efficient. As set lookups are O(1) you iterate over the set once and for each entry check if 2020 - entry is also in the set. This makes the time complexity for part one linear. Part two could be improved even more. I still use combinations, but of only 2 entries. Then for each combination check if 2020 - sum(combination) is in the set.<br>
Compared to brute force the final solution for part one is 100 times faster and for part two 400 times.<br>
*(total runtime: 1.6ms)*

### Day 2: [Password Philosophy](https://adventofcode.com/2020/day/2)
The Toboggan rental office needs you to do password validation for them. You are given a list of strings, where each line contains a password and the policy it needs to comply with.<br>
First I converted the password-policy strings into namedtuples. After that the rest of the problem is straightforward.
Initially I used a separate function for the validation of part two, but by using exclusive or (XOR) I was able to get rid of that. This made the code more readable and also slightly faster. Part two policy indexes from 1, so the function needs to account for that.<br>
*(total runtime: 4.25ms)*

### Day 3: [Toboggan Trajectory](https://adventofcode.com/2020/day/3)
You take a toboggan (sled) to the airport, but steering is hard. You receive tree coordinates and need to calculate how many trees you are likely to hit on a given trajectory. The map you receive is incomplete. If you go off the map on the Eastern edge before reaching the Southern edge you need to revert to the Western edge. This can be achieved by applying modulo to the column (EAST-WEST) index of the grid.<br>
Only one function is needed for both parts, as the trajectories parameter is a list. For part one there is 1 trajectory and for part two there are 5.<br>
*(total runtime: 0.49ms)*

### Day 4: [Passport Processing](https://adventofcode.com/2020/day/4)
On day four you arrive at the airport and end up in a very long line for the passport scanners. You can speed up your progress by helping out with passport validation.
The function for part one converts the strings with passport data to a dictionary. If this dictionary contains all the required fields it is added to a list. This list is the input for part two. The answer for part one is the length of this list.
For part two I used TDD (Test Driven Development) with pytest. For every validation (hair color, height etc) I wrote a separate function that could be tested. All 7 validation functions are then applied to every passport. Only passports for which all 7 validations return True are counted.<br>
*(total runtime: 2.07ms)*

### Day 5: [Binary Boarding](https://adventofcode.com/2020/day/5)
When you board the plane you discover that you dropped your boarding pass. Based on nearby boarding passes you attempt to discover your seat.<br>
The problem description immediately led me down the binary search path. This worked fine. After finding the solution, I discovered that the boarding pass string is actually a binary number, where Bs and Rs are ones and Fs and Ls are zeros. Hand smacks head! That would have made solving it a lot easier. Converting binary to int is very easy in python. Just add 2 (binary is base 2) as second parameter to the int function.<br>
*(total runtime: 1.58ms)*

### Day 6: [Custom Customs](https://adventofcode.com/2020/day/6)
You end up helping the whole plane with their customs declaration forms.<br>
For part one you need to count the questions to which ANYONE in a group of passengers answered yes. For part two you need to count the question where EVERYONE in the group answered yes. This can be solved quite easily with sets. Part one is the union and part two the intersection.<br>
*(total runtime: 3.77ms)*

### Day 7: [Handy Haversacks](https://adventofcode.com/2020/day/7)
Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags.<br>
I converted the input data to a graph that holds the quantities of other bags each bag can hold. For part one, you need to count how many bags directly or indirectly contain one shiny gold bag? To solve this I applied bfs to every bag and increased the count by 1 if it found a shiny gold bag. This algorithm is not very efficient, as it does not do any memoization. If a blue bag holds an orange bag that holds a shiny gold bag, then both the blue and orange bag should be counted. However, the algorithm still investigates the orange bag, even though it already saw it when searching the blue bag. The simplest way to make this more efficient may be to go backward. In other words, start at the shiny gold bag, add all its parents and add them to the count, then find all their parents and add them, etc. However, as the performance of the algorithm is not too bad (14ms), I will not do this at this time.<br>
For part two you need to find how many bags the shiny gold bag holds in total. The tricky bit here is that for every bag you need to keep track of how often it's parent is present. Let's say the shiny gold bag holds 2 green bags and each green bag holds 3 yellow bags. In this example, shiny gold holds 8 bags in total (2 green and 6 yellow). I used a queue for this problem. Every time a bag is popped of the queue it's value is added to the count. Then all its children are added to the queue. The value for each child is the product of its own and it's parents value. The count is returned when all bags have been seen (the queue is empty). This algorithm is quite efficient (0.04ms), as it sees every bag only once. What also helps is that the search space is smaller than in part one, as only the content of the shiny gold bag needs to be searched.<br>
*(total runtime: 17.14ms)*

### Day 8: [Handheld Halting](https://adventofcode.com/2020/day/8)
During your flight, the kid next to you needs help with his handheld game console. You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device.<br>
Every line of the bootcode has one instruction. For part one, you need to find the first line (instruction) in the boot code that repeats and return what the value of the accumulator is at that time. This can be solved by adding every line that is visited to a set. Execute the bootcode line for line in a while loop and break out of the loop as soon as you visit a line that was seen before (is in the set).<br>
For part two you need to figure out which line of the bootcode is wrong. If the bootcode reaches its last line it is correct. If the bootcode ends up in an infinite loop, as in part one, it is wrong. A simple brute force solution changes one line at the time and tests whether the bootcode performs correctly. This solves the problem in about 18ms, which is not too bad. It is not obvious to me how you could improve on this.<br>
This problem was quite similar to the many int code problems in AoC 2019. Many AoC-ers, including me, suspected we might see more bootcode problems as well. Therefore, I refactored my solution to a class. Of course, no other bootcode problems were seen... Well played Eric!<br>
*(total runtime: 18.8ms)*
