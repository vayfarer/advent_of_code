# Advent of Code 2022, Day 18, Part 1 and 2
# Michael Chen
# 12/18/2022

class Obsidian:
    def __init__(self, coordinates):
        """Creates an obsidian object located at `coordinates`"""
        self.location = coordinates
        self._adjacent = set()
        self._all_sides = set()
        self._open_sides = set()
        self.add_sides()

    def __str__(self):
        """Printable object information"""
        return "Obsidian block at " + str(self.location)

    def count(self):
        """Returns the number of open sides."""
        return len(self._open_sides)

    def add_sides(self):
        """Adds adjacent locations. Assume they start as open sides."""
        l_coords = list(self.location)
        for i, n in enumerate(l_coords):
            l_coords[i] += 1
            self._all_sides.add(tuple(l_coords))
            l_coords[i] += -2
            self._all_sides.add(tuple(l_coords))
            l_coords[i] += 1

            # all sides start as open sides.
        self._open_sides = self._all_sides.copy()

    def add_adjacent(self, block):
        """Checks if a block is adjacent. Adds an adjacent block. Moves the
         appropriate side from _open_sides to _adjacent."""

        if block.location in self._adjacent:
            # already added.
            print("Add adjacent operation " + str(block) + " already in " + self.__str__())

        if block.location in self._open_sides:
            # not yet added.
            self._open_sides.remove(block.location)
            self._adjacent.add(block.location)

    def all_sides(self):
        """Returns the set of open sides"""
        return self._all_sides

    def open_sides(self):
        """Returns the set of open sides"""
        return self._open_sides

class Water(Obsidian):
    def __init__(self, coordinates, min_boundary, max_boundary):
        """Creates a water object located at `coordinates`"""
        self._obsidian = set()
        self._min_boundary = min_boundary
        self._max_boundary = max_boundary
        super().__init__(coordinates)

    def __str__(self):
        """Printable object information"""
        return "Water block at " + str(self.location)

    def add_sides(self):
        """Adds adjacent locations. Assume they start as open sides."""
        l_coords = list(self.location)
        for i, n in enumerate(l_coords):
            l_coords[i] += 1
            if l_coords[i] <= self._max_boundary[i]:
                self._all_sides.add(tuple(l_coords))
            l_coords[i] += -2
            if l_coords[i] >= self._min_boundary[i]:
                self._all_sides.add(tuple(l_coords))
            l_coords[i] += 1

        # all sides start as open sides.
        self._open_sides = self._all_sides.copy()

    def add_obsidian(self, block):
        """Checks if an obsidian block is already added. Then adds it. Moves
        the appropriate side from _open_sides to _obsidian."""

        if block.location in self._obsidian:
            # already added.
            print("Add obsidian operation " + str(block) + " already in " + self.__str__())

        if block.location in self._open_sides:
            # not yet added.
            self._open_sides.remove(block.location)
            self._obsidian.add(block.location)

    def count_obsidian(self):
        """Returns the number of sides in contact with obsidian."""
        return len(self._obsidian)

class Pond:
    """Contains obsidian blocks"""
    def __init__(self):
        """Creates a pond full of obsidian and water blocks"""
        self._blocks = {}
        self._water = {}

    def add(self, coordinates):
        """Adds an obsidian block at `coordinates`. Coordinates is tuple (x,y,z)"""
        new_block = Obsidian(coordinates)
        # Only add the block if it doesn't already exist.
        self._blocks.setdefault(new_block.location, new_block)

        # Checks all sides of new block for existing adjacent blocks.
        for side in new_block.all_sides():
            side_block = self._blocks.get(side, False)
            if side_block:
                side_block.add_adjacent(new_block)
                new_block.add_adjacent(side_block)

    def surface_area(self):
        """Counts all open surfaces."""
        surface_area = 0
        for block in self._blocks.values():
            surface_area += block.count()
        return surface_area

    def water(self):
        """Surrounds the obsidian with water to count the external obsidian to
        water surface area."""
        x,y,z = [n[0] for n in self._blocks], [n[1] for n in self._blocks], [n[2] for n in self._blocks]
        self._water_min = min(x) - 1, min(y) - 1, min(z) - 1
        self._water_max = max(x) + 1, max(y) + 1, max(z) + 1

        # fill exterior space with water!
        queue = {self._water_min}
        while queue:
            self.add_water(queue, self._water_min, self._water_max)

    def add_water(self, queue, min_boundary, max_boundary):
        """Adds a block of water, populates queue with additional space for water"""
        new_block = Water(queue.pop(), min_boundary, max_boundary)
        # Only add the block if it doesn't already exist.
        self._water.setdefault(new_block.location, new_block)

        # Checks all sides of new block for existing adjacent blocks.
        for side in new_block.all_sides():
            obsidian_block = self._blocks.get(side, False)
            if obsidian_block:
                # adjacent obsidian block
                new_block.add_obsidian(obsidian_block)
            else:
                water_block = self._water.get(side, False)
                if water_block:
                    # adjacent water block
                    water_block.add_adjacent(new_block)
                    new_block.add_adjacent(water_block)
                elif side not in queue:
                    queue.add(side)

    def water_surface_area(self):
        """Counts surfaces of water in contact with obsidian."""
        pond.water()
        surface_area = 0
        for block in self._water.values():
            surface_area += block.count_obsidian()
        return surface_area

if __name__ == "__main__":

    blocks = []

    with open('input.txt') as f:
        line = f.readline().strip()
        while line:
            blocks.append(line)
            line = f.readline().strip()

    for i, line in enumerate(blocks):
        blocks[i] = tuple(int(n) for n in line.split(sep=','))

    pond = Pond()
    for block in blocks:
        pond.add(block)

    # part 1
    print('Surface area of obsidian in the pond is ' + str(pond.surface_area()))

    # Part 2
    print('Exterior surface area of obsidian in contact with water is '+ str(pond.water_surface_area()))





