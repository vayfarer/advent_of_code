# Advent of Code 2022, Day 1 Part 1 and 2
# Michael Chen
# 12/23/2022

calories = 0
big_cal = [0, 0, 0]

with open('input.txt') as f:
    input1 = f.read()

lines = input1.split('\n')

for line in lines:
    line = line.strip()
    if line:
        # empty string evaluates as false.
        calories += int(line)
    else:
        i = 3
        while i > 0 and calories > big_cal[i - 1]:
            # Check against current highest calories from bottom up.
            i -= 1
        big_cal.insert(i, calories)
        big_cal.pop(3)
        calories = 0

print(f'The most calories a single elf is carrying is {big_cal[0]}.')
print(f'The elves with the top 3 calories are carrying {sum(big_cal)} calories.')