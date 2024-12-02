# Advent of Code 2022, Day 2 Part 1
# Michael Chen
# 12/25/2022

# A,X rock
# B,Y paper
# C,Z scissors

scoring = {'A X':4,
          'A Y':8,
          'A Z':3,
          'B X':1,
          'B Y':5,
          'B Z':9,
          'C X':7,
          'C Y':2,
          'C Z':6}

with open('input.txt') as f:
    input_list = f.read().strip().split('\n')

score = 0
for line in input_list:
    score += scoring[line]

print(f'Part 1 total score: {score}')

# X lose
# Y draw
# Z win

scoring2 = {'A X': 'A Z',
            'A Y': 'A X',
            'A Z': 'A Y',
            'B X': 'B X',
            'B Y': 'B Y',
            'B Z': 'B Z',
            'C X': 'C Y',
            'C Y': 'C Z',
            'C Z': 'C X'}

score = 0
for line in input_list:
    score += scoring[scoring2[line]]

print(f'Part 2 total score: {score}')






