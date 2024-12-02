# Advent of Code 2022, Day 17, Part 1 and 2
# Michael Chen
# 12/17/2022

import time

class RockError(Exception):
    """Problem with the rock object"""
    pass

class Rock:

    def __init__(self, origin, shape):
        """
        Rock object. Initiate to location and shape.
        :param origin: (x, y) coordinates of rock origin (bottom left corner)
        :param shape: int 0 to 4, 0: _, 1: +, 2: ┘, 3: |, 4:square
        """
        self.x = origin[0]
        self.y = origin[1]
        self._shape = shape

        # create list of coordinates which are rocks.

        match shape:
            case 0: # _
                self._ref_coord = [(0,0), (1,0), (2,0), (3,0)]
                self.height = 1
            case 1: # +
                self._ref_coord = [(0,1), (1,2), (1,1), (1,0), (2,1)]
                self.height = 3
            case 2: # ┘
                self._ref_coord = [(0,0), (1,0), (2,0), (2,1), (2,2)]
                self.height = 3
            case 3: # |
                self._ref_coord = [(0,0), (0,1), (0,2), (0,3)]
                self.height = 4
            case 4: # square
                self._ref_coord = [(0,0), (1,0), (0,1), (1,1)]
                self.height = 2
            case _:
                raise RockError

        self._rock_coord = self._ref_coord.copy()
        # moves coordinates to origin location.
        self.update_coordinates()

    def __str__(self):
        """Printable object information"""
        out = f'Rock object shape {self._shape} at ({self.x}, {self.y}:  '
        out += str(self._rock_coord)
        return out

    def coordinates(self):
        """Returns the current coordinates"""
        return self._rock_coord

    def next_coordinates(self, move):
        """Returns the coordinates of the rock if it were to move according to
        `move` parameter. `move` parameter is (x, y)"""
        moved_coordinate = []
        for x, y in self._rock_coord:
            moved_coordinate.append((x + move[0], y + move[1]))
        return moved_coordinate

    def update_coordinates(self):
        """Translates coordinates to the current origin location."""
        for i in range(len(self._ref_coord)):
            self._rock_coord[i] = (self._ref_coord[i][0]+self.x, self._ref_coord[i][1]+self.y)

    def move(self, move):
        """Moves the rock object according to `move` parameter."""
        self.x += move[0]
        self.y += move[1]
        self.update_coordinates()

    def origin(self):
        """Returns the origin coordinate of the rock"""
        return self.x, self.y

    def top(self):
        """Returns the top elevation of the rock"""
        return self.y + self.height

    def shape(self):
        return self._shape

class Chamber:

    def __init__(self):
        """Inits a chamber."""
        self._rows=[]
        self._height = 0
        self._multiplier = 0
        self._mem_limit = 100000
        # create some empty rows
        self.append_rows(7)

    def __str__(self):
        """Prints 10 lines of the chamber with rocks"""
        out = ''
        i = 0
        for row in self._rows[-1:-11:-1]:
            out += "".join(row) + str(self._height - i) + '\n'
            i += 1
        return out

    def append_rows(self, n):
        """Adds empty rows to the top of the chamber."""
        if n > 0:
            for i in range(n):
                self._rows.append(['|'] + ['.']*7+['|'])
            self._height = len(self._rows)

        if self._height > self._mem_limit * 2:
            self._rows = self._rows[self._mem_limit:]
            self._height = len(self._rows)
            self._multiplier += 1

    def top_rock(self):
        """Returns the elevation of the top rock piece."""
        top = len(self._rows)

        while top !=0  and '#' not in self._rows[top-1]:
            top -= 1

        return top

    def multiply_top(self):
        """Returns the total rows reach including the truncated rows"""
        return self._multiplier * self._mem_limit + self.top_rock()

    def spawn_rock(self, shape):
        """Creates a rock"""
        self.append_rows(7- (self._height - self.top_rock()))

        origin_x = 3
        origin_y = self.top_rock() + 3

        rock = Rock((origin_x,origin_y), shape)

        self.append_rows(rock.top() - self._height)
        self.draw_rock(rock)

        return rock

    def draw_rock(self, rock):
        """Draws a rock in the rows"""
        rock_coord = rock.coordinates()
        for x,y in rock_coord:
            self._rows[y][x] = '@'

    def undraw_rock(self, rock):
        """Undraws a rock"""
        rock_coord = rock.coordinates()
        for x,y in rock_coord:
            self._rows[y][x] = '.'

    def move_rock(self, rock:Rock, move):
        """
        Move a rock if able.
        :param rock: Rock object to be moved.
        :param move: (x, y) move of rock
        :return: True if can continue moving, False if not.
        """

        # check if rock collides due to move.
        if self.check_collision(rock.next_coordinates(move)):
            if move[1] == -1:
                # Rock collides moving down.
                self.rock_fallen(rock)
                return False
            # Rock collision sideways do nothing.
            return True

        # Move the rock.
        self.undraw_rock(rock)
        rock.move(move)
        self.draw_rock(rock)
        return True

    def check_collision(self, rock_coord):
        """Returns True if collision will occur, false if not."""

        for x,y in rock_coord:
            if self._rows[y][x] in '#|' or y < 0:
                return True
        return False

    def rock_fallen(self, rock):
        """Converts a rock into a fallen rock"""
        rock_coord = rock.coordinates()
        for x,y in rock_coord:
            self._rows[y][x] = '#'
        del rock

def pattern_move(s):
    """Translates the pattern character into a move"""
    if s == '>':
        return 1,0
    elif s == '<':
        return -1,0

def simulate_rocks(number_rocks, pattern):
    """Simulates the rocks falling in the chamber
    Tries to find a repeating pattern for very large number of rocks."""

    len_pattern = len(pattern)
    num_shapes = 5

    # initiating loop variables.
    chamber = Chamber()
    pattern_index = 0
    shape = 0

    # simulation repeat detection variables
    old_i = 0
    delta_i = []
    shapes = []
    delta_h = []
    old_height = chamber.top_rock()
    min_sims = num_shapes
    if len_pattern < 5000:
        min_sims = (5000//len_pattern) * min_sims
    sim_count = 0

    # start simulating rocks
    for i in range(number_rocks):
        rock = chamber.spawn_rock(shape)
        shape = (shape + 1) % 5
        falling = True

        while falling:

            # move rock to side based on pattern.
            chamber.move_rock(rock, pattern_move(pattern[pattern_index]))
            pattern_index = (pattern_index + 1) % len_pattern

            if pattern_index == 0:
                #cycled through the pattern once
                sim_count += 1
                if sim_count % min_sims == 0:
                    #cycled through the pattern by the amount of shapes.

                    delta_i.append(i-old_i)
                    old_i = i
                    height = chamber.multiply_top()
                    delta_h.append(height - old_height)
                    old_height = height
                    shapes.append(rock.shape())

                    if len(delta_i) >2:
                        # collected 3 cycles.
                        # check if cycles 2 and 3 are the same.
                        if delta_i[1] == delta_i[2] and delta_h[1] == delta_h[2] and shapes[1] == shapes[2]:
                            # pattern achieved.
                            cycles = number_rocks // delta_i[1]
                            cycle_height = delta_h[1]
                            remainder = (number_rocks - delta_i[0]) % (delta_i[1])

                            init_plus_rem = simulate_rocks(delta_i[0] + remainder, pattern)

                            total = (cycles - 1) * cycle_height + init_plus_rem
                            return total

                        print('simulation failed.')

            # move rock down. If rock cannot move down, then falling set to False.
            falling = chamber.move_rock(rock, (0, -1))

    print(chamber)
    return chamber.multiply_top()


if __name__ == "__main__":
    start = time.perf_counter()
    # pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

    file = open('input.txt', mode = 'r')
    pattern = file.readline().strip()
    num_rocks = 1000000000000

    height = simulate_rocks(num_rocks,pattern)
    print(f'Pile of rocks is {height} tall. ')
    print(f'Simulation time {time.perf_counter() - start} seconds. ')


