# Advent of Code 2022, Day 16, Part 1 and 2
# Michael Chen
# 12/21/2022
# *Part 2 solution edge and corner cases not complete.

class Sensor:
    def __init__(self, x:int, y:int, radius:int):
        self.x, self.y = x, y
        self.radius = radius
        self.contained = False

    def __str__(self):
        return str(self.coords())

    def coords(self):
        """Returns x,y coordinates of the sensor."""
        return (self.x, self.y)

    def contains(self, other_sensor):
        """Returns true if the scope of this sensor contains other_sensor"""
        if manhattan(self.coords(), other_sensor.coords()) + other_sensor.radius <= self.radius:
            other_sensor.contained = True
            return True
        else:
            return False

class Beacon:
    def __init__(self, point):
        """Creates a beacon point to interact with Sensor.contains( )"""
        self.x, self.y = point[0], point[1]
        self.radius = 0

    def coords(self):
        return (self.x, self.y)

class InvalidPair(Exception):
    """Invalid Pair"""
    pass

class Pair:
    """A pair of sensors with a manhattan gap of 2 between their radius"""
    def __init__(self, sensor1, sensor2):
        self.distance = manhattan(sensor1.coords(), sensor2.coords())
        if self.distance != sensor1.radius + sensor2.radius + 2:
            raise InvalidPair

        self._equal = False
        self._line_between = []

        if sensor1.y < sensor2.y:
            self._low_point = sensor1
            self._high_point = sensor2
        elif sensor1.y == sensor2.y:
            # case where the sensors are on the same elevation, confining only
            # one point between them.
            self._equal = True
            if sensor1.x < sensor2.x:
                self._line_between.append((sensor1.x + sensor1.radius + 1, sensor1.y))
            else:
                self._line_between.append((sensor2.x + sensor2.radius + 1, sensor2.y))
        else:
            self._low_point = sensor2
            self._high_point = sensor1

        if self._low_point.x < self._high_point.x:
            self._high_right = True
        elif sensor1.x == sensor2.x:
            self._equal = True
            if sensor1.y < sensor2.y:
                self._line_between.append((sensor1.x, sensor1.y + sensor1.radius + 1))
            else:
                self._line_between.append((sensor2.x, sensor2.y + sensor2.radius + 1))
        else:
            self._high_right = False

        if self._equal:
            self._line_between.append(self._line_between[0])

    def __str__(self):
        return str(self._low_point) + ' ' + str(self._high_point)

    def slope(self):
        """Returns the slope of the line confined between the two points"""
        if self._equal:
            # single point, undefined slope.
            return 0
        return -1 if self._high_right else 1

    def between(self)->list:
        """Returns a pair of points defining a line contacting both sensors in
         the pair"""

        if self._line_between:
            # already computed before.
            return self._line_between

        # low side is either defined by which lowest confining space of either
        # point is also confined by the other point.
        low_ends = [(self._low_point.x + self._low_point.radius, self._low_point.y+1),
                   (self._low_point.x - self._low_point.radius, self._low_point.y+1),
                   (self._high_point.x + 1, self._high_point.y - self._high_point.radius),
                   (self._high_point.x - 1, self._high_point.y - self._high_point.radius)
                   ]

        low_end = None

        for end in low_ends:
            if manhattan(end, self._low_point.coords()) - self._low_point.radius == manhattan(end, self._high_point.coords()) - self._high_point.radius:
                # distance to both points - point radius should equal 1.
                if low_end and end[1] > low_end[1]:
                    # pick the higher low end if there's two.
                    low_end = end
                else:
                    low_end = end

        high_ends = [(self._low_point.x + 1, self._low_point.y + self._low_point.radius),
                    (self._low_point.x - 1, self._low_point.y + self._low_point.radius),
                    (self._high_point.x + self._high_point.radius, self._high_point.y - 1),
                    (self._high_point.x - self._high_point.radius, self._high_point.y - 1)
                    ]

        high_end = None

        for end in high_ends:
            if manhattan(end, self._low_point.coords()) - self._low_point.radius == manhattan(end, self._high_point.coords()) - self._high_point.radius:
                # distance to both points - point radius should equal 1.
                if high_end and end[1] < high_end[1]:
                    # pick the lower high end if there's two.
                    high_end = end
                else:
                    high_end = end

        self._line_between = [low_end, high_end]
        return self._line_between

    def intersect(self, other_pair):
        """Returns false if there is no intersection between the line defined by
        this pair and other pair. Returns the intersecting point otherwise. """
        if self.slope() == other_pair.slope():
            if self.between()[0] == other_pair.between()[0] and self.slope() == 0:
                # case where both pairs confine only one point
                return self.between()[0]
            return False

        if manhattan(self.between()[0], other_pair.between()[0]) %2 == 1:
            # Offset by odd manhattan distance, cannot intersect.
            return False

        if self.slope() == 1:
            up_line, down_line = self.between(), other_pair.between()
        else:
            up_line, down_line = other_pair.between(), self.between()
        # the up_line goes up from left to right

        if down_line[0][0] - up_line[0][0] + up_line[0][1] < down_line[0][1]:
            # the down pair lower point is above the up pair line and does not
            # intersect
            return False

        if down_line[1][0] - up_line[0][0] + up_line[0][1] > down_line[1][1]:
            # the down pair upper point is below the up pair line and does not
            # intersect
            return False

        if up_line[1][1] < -up_line[1][0] + down_line[0][0] + down_line[0][1]:
            # the up pair upper point is below the down pair line.
            return False

        if up_line[0][1] > -up_line[0][0] + down_line[0][0] + down_line[0][1]:
            # the up pair lower point is above the down pair line.
            return False

        if up_line[0][1] <= down_line[0][1]:
            d = manhattan(up_line[0], down_line[0]) // 2 # guaranteed this is even earlier.
        else:
            d = manhattan(up_line[0], down_line[0]) // 2 - (up_line[0][1] - down_line[0][1])

        return up_line[0][0] + d, up_line[0][1] + d


def manhattan(a, b):
    """Returns the manhattan distances between point a and point b, which are
    in format tuple(x, y) coordinates."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


if __name__ == "__main__":

    y_line = 2000000

    sensors = set()
    no_beacon = 0
    no_beacon_runs = {(0,-1)}
    beacons_on_line = set()

    with open('input.txt') as f:
        line = f.readline().strip()
        while line:

            s_x, aa, line = line.partition(',')
            s_y, aa, line = line.partition(':')
            s_x = int(s_x.partition('x=')[2])
            s_y = int(s_y.partition('y=')[2])

            b_x, aa, b_y = line.partition(',')
            b_y = int(b_y.partition('y=')[2])
            b_x = int(b_x.partition('x=')[2])

            # Handles case where beacon is on the y_line, for Part 1
            if b_y == y_line:
                beacons_on_line.add(b_x)

            new_sensor = Sensor(s_x, s_y, manhattan((s_x, s_y), (b_x, b_y)))

            # Prune sensors which are encompassed by other sensors.
            remove_sensors = set()
            for sensor in sensors:
                if sensor.contains(new_sensor):
                    break
                elif new_sensor.contains(sensor):
                    remove_sensors.add(sensor)

            # can't change set size during iteration
            sensors.difference_update(remove_sensors)
            if not new_sensor.contained:
                sensors.add(new_sensor)

            line = f.readline().strip()

    for sensor in sensors:
        dy = abs(y_line - sensor.y)
        if sensor.radius >= dy:
            dx = abs(sensor.radius - dy)
            x_start, x_end = sensor.x - dx, sensor.x + dx

            for run in no_beacon_runs.copy():
                if run[0] <= x_start <= run[1] <= x_end:
                    no_beacon_runs.remove(run)
                    x_start = run[0]
                elif x_start <= run[0] <= x_end <= run[1]:
                    no_beacon_runs.remove(run)
                    x_end = run[1]
                elif run[0] <= x_start and x_end <= run[1]:
                    x_start, x_end = run[0], run[1]
                elif x_start <= run[0] <= run[1] <= x_end:
                    no_beacon_runs.remove(run)

            no_beacon_runs.add((x_start,x_end))

    # dummy run to trigger loop conditions above.
    no_beacon_runs.remove((0,-1))

    for run in no_beacon_runs.copy():
        no_beacon += run[1] - run[0] + 1

    # remove any beacons which occur on the line.
    for beacon in beacons_on_line:
        for run in no_beacon_runs:
            if run[0] <= beacon <= run[1]:
                no_beacon -=1
                break

    print(f'{no_beacon} points cannot be beacons on line {y_line}') #5525990

    # If the missing beacon occurs in the middle of the space, it must be
    # contained by two pairs of sensors which are exactly two apart in coverage.
    sensors_searched = sensors.copy()
    pairs = set()

    for sensor_i in sensors:
        sensors_searched.remove(sensor_i)
        for sensor_j in sensors_searched:
            if manhattan(sensor_i.coords(), sensor_j.coords()) == sensor_i.radius + sensor_j.radius + 2:
                pairs.add(Pair(sensor_i, sensor_j))

    # Turns out there are two pairs found in my input.
    other_pairs = pairs.copy()
    intersections = set()

    for pair_i in pairs:
        other_pairs.remove(pair_i)
        for pair_j in other_pairs:
            point = pair_i.intersect(pair_j)
            if point:
                intersections.add(Beacon(point))

    for point in intersections.copy():
        for sensor in sensors:
            if sensor.contains(point):
                intersections.difference_update({point})
                break

    if len(intersections) == 1:
        missing_beacon = intersections.pop()
        print(f'Missing beacon frequency is {missing_beacon.x*4000000 + missing_beacon.y}')
    elif len(intersections) > 1:
        print('Isolated more than one missing beacon.')
    else:
        print('Missing beacon not found!!')

    # prototype code for literal edge and corner cases.
    # If the missing beacon is not found confined by pairs, then it might still
    # be confined on an edge or a corner.
    # If the missing beacon occurs on the edge, it must be confined by 2
    # beacons on the edge, or one beacon on the corner. The missing beacon can
    # only occur just outside the intersection of the sensors and the edge.

    # beacons intercepting the y = 4000000 line
    # y4_sensors = set()
    # for sensor in sensors:
    #     if sensor.radius >= abs(000000 - sensor.y):
    #         y4_sensors.add(sensor)
    #
    # y0_xs = set()
    # y0_doubles = set()
    #
    # for sensor in y4_sensors:
    #     dy = abs(000000 - sensor.y)
    #     dx = abs(sensor.radius - dy)
    #     xs = sensor.x - dx - 1, sensor.x + dx + 1
    #     for x in xs:
    #         if 0 <= x <= 4000000:
    #             if x not in y0_xs:
    #                 y0_xs.add(x)
    #             else:
    #                 y0_doubles.add(x)
    #
    #
    # for x in y0_xs:
    #     missing = True
    #     for sensor in y4_sensors:
    #         if manhattan((x, 000000), sensor.coords()) <= sensor.radius:
    #             missing = False
    #             # print(x,sensor)
    #     if missing:
    #         print(f'found! {x}')
    #
    #
    # # beacons intercepting the x = 4000000 line
    # x4_sensors = set()
    # for sensor in sensors:
    #     if sensor.radius >= abs(000000 - sensor.x):
    #         x4_sensors.add(sensor)
    #
    # x0_ys = set()
    # x0_doubles = set()
    #
    # for sensor in x4_sensors:
    #     dx = abs(000000 - sensor.x)
    #     dy = abs(sensor.radius - dx)
    #     ys = sensor.y - dy - 1, sensor.y + dy + 1
    #     for y in ys:
    #         if 0 <= y <= 4000000:
    #             if y not in x0_ys:
    #                 x0_ys.add(y)
    #             else:
    #                 x0_doubles.add(y)
    #
    # for y in x0_ys:
    #     missing = True
    #     for sensor in x4_sensors:
    #         if manhattan((000000, y), sensor.coords()) <= sensor.radius:
    #             missing = False
    #     if missing:
    #         print(f'found! {y}')
    #
    #
    # for x in range(4000000):
    #     missing = True
    #     for sensor in sensors:
    #         if manhattan((x, 0), sensor.coords()) <= sensor.radius:
    #             missing = False
    #     if missing:
    #         print(f"({x}, 0")
    #
    #     missing = True
    #     for sensor in sensors:
    #         if manhattan((x, 4000000), sensor.coords()) <= sensor.radius:
    #             missing = False
    #     if missing:
    #         print(f"({x}, 4000000")
    #

