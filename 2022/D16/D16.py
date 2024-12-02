# Advent of Code 2022, Day 16, Part 1
# Michael Chen
# 12/16/2022

class Valve:
    def __init__(self, id: str, flow: int, time: int):
        """inits a valve object"""
        self._id = id
        self._flow = flow
        self._time = time
        self._valve_times = []
        self._adjacents = []
        self._open = False

        # data member used for distance mapping.
        self.distance = 0
        self.path = []

        for minute in range(time):
            self._valve_times.append((self._time - minute - 1) * self._flow)

    def __str__(self):
        """Provides readable print"""
        out = ''
        out += f'Valve {self._id} '
        out += f'Flow {self._flow} Adjacents '
        for valve in self._adjacents:
            out += valve.name() + ' '
        return out

    def volume(self, minute):
        """Returns the amount of volume released by opening this valve at the
        specified `minute`"""

        return self._valve_times[minute] if not self._open else 0

    def add_adjacent(self, valve):
        """adds an adjacent Valve object"""
        if valve not in self._adjacents:
            self._adjacents.append(valve)

    def adjacents(self) -> list:
        """Returns a list of adjacent valves"""
        return self._adjacents

    def add_distances(self):
        """Creates a dictionary for distances and paths to all connected
         valves
         {to Valve ID : (valve distance, path to valve, valve object)}"""

        queue = [self]
        self._distances = {}
        queue[0].distance = 0
        queue[0].path = []

        while queue:
            valve = queue.pop(0)
            if valve.name() not in self._distances or valve.distance < self._distances[valve.name()][0]:
                self._distances[valve.name()] = (valve.distance, valve.path, valve)

            for adjacent in valve.adjacents():
                if adjacent.name() not in self._distances and adjacent not in queue:
                    # since this tree has equal traversal times, any earlier instance
                    # should have been the faster travel time.
                    adjacent.path = valve.path.copy()
                    adjacent.path.append(adjacent)
                    adjacent.distance = valve.distance + 1
                    queue.append(adjacent)

    def distance_to(self, valve:str=None):
        """Returns the distance to a certain valve, or all of them"""
        if valve is None:
            return self._distances

        return self._distances[valve]

    def next_step_to(self, valve: str):
        """Returns the next step to a certain valve"""
        return self._distances[valve][1][0]

    def name(self):
        """Returns the valve ID"""
        return self._id

    def is_open(self):
        return self._open

    def open(self):
        """Opens the valve"""
        self._open = True

    def close(self):
        self._open = False

def volumes_from_valve(this_valve, minute, max_depth):
    """Returns a sorted queue of valves from this valve, of volumes released by
    traversing to that valve and opening it"""

    volumes = {}

    for name, distance in this_valve.distance_to().items():
        if minute + distance[0] < max_depth:
            volumes[distance[2]] = distance[2].volume(minute + distance[0])
        else:
            volumes[distance[2]] = 0

    sorted_volumes = sorted(volumes.items(), key=lambda x:x[1], reverse=True)
    queue = list(filter(lambda c: c[1] > 0, sorted_volumes))

    return queue

def go_to_valve_open(this_valve, target_valve, path):
    """Goes to the target valve and opens it."""
    if target_valve is this_valve:
        path.append(f"OPEN {target_valve.name()}")
        target_valve.open()
    elif target_valve:
        next_valve = this_valve.next_step_to(target_valve.name())
        path.append(f"MOVE {next_valve.name()}")
        go_to_valve_open(next_valve, target_valve, path)

def dfs(start_valve, max_depth, sum, path:list, max_path, max_sum = 0):
    """
    DFS to find the most pressure released
    """

    # time is measured by length of path
    minute = len(path)
    queue = volumes_from_valve(start_valve, minute, max_depth)

    while queue and minute < max_depth:
        valve, volume = queue.pop(0)
        # print(f'Minute: {minute} Sum: {sum}', " to: ", valve, '+',volume )

        # creating new string to avoid string mutability problems.
        new_path = path.copy()
        go_to_valve_open(start_valve, valve, new_path)
        sum += volume
        # print(sum, new_path)

        max_sum, max_path = dfs(valve, max_depth, sum, new_path, max_path, max_sum)
        # Need to close the valve and back out after recursing.
        valve.close()
        sum -= volume

    else:
        if sum > max_sum:
            max_sum, max_path = sum, path

    if len(max_path) < max_depth:
        for i in range(len(max_path), max_depth):
            max_path.append('DO NOTHING')

    return max_sum, max_path

if __name__ == "__main__":

    # # example valve data
    # valve_data = {
    #     'AA': (0, {'DD', 'II', 'BB'}),
    #     'BB': (13, {'CC', 'AA'}),
    #     'CC': (2, {'DD', 'BB'}),
    #     'DD': (20, {'CC', 'AA', 'EE'}),
    #     'EE': (3, {'FF', 'DD'}),
    #     'FF': (0, {'EE', 'GG'}),
    #     'GG': (0, {'FF', 'HH'}),
    #     'HH': (22, {'GG',}),
    #     'II': (0, {'AA', 'JJ'}),
    #     'JJ': (21, {'II',}),
    # }

    start = 'AA'
    time = 30
    valves = []
    valve_data = {}
    valve_matrix = {}
    valve_distances = {}

    file = open('input.txt', mode = 'r')

    line = file.readline()

    while line:
        valve_name = line[6:8]
        valve_flow = line[23:25]
        valve_flow = int(valve_flow.strip(';'))
        valve_adj = line.partition('to valve')[2]
        valve_adj = valve_adj.strip('s \n').split(', ')

        valve_data[valve_name] = (valve_flow, valve_adj)
        valve_matrix[valve_name] = Valve(valve_name, valve_flow, time)

        line = file.readline()

    # add valve adjacents
    for name, valve in valve_matrix.items():
        for adjacent in valve_data[name][1]:
            valve.add_adjacent(valve_matrix[adjacent])

    # compute valve distances
    for name, valve in valve_matrix.items():
        valve.add_distances()
        print(valve)

    print('Valves Loaded.')

    # starting valve location
    location = valve_matrix[start]

    # compute optimal solution
    volume, path = dfs(location, time, 0, [], [])
    print(f"Route: {path}")
    print(f"Total Pressure Released: {volume}") # 2330



