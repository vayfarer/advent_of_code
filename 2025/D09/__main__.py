from utility import get_lines, input_arg_parse
from heapq import heappush, heappop
import time


class GridSet:
    def __init__(self):
        self._out = set()
        self._x_edge = set()
        self._y_edge = set()
        self._edge = set()

    def process_edges(self):
        """
        Iterate through edge tiles.
        Add adjacents to edge adjacent set if it's not in the edge set.
        Process all the adjacent tiles and add to the out set if it's out of the shape...
        """
        edge_adj_tiles = set()
        adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for tile in self._edge:
            x, y = tile
            for dx, dy in adjacents:
                adj_tile = (x + dx, y + dy)
                if adj_tile not in self._edge:
                    edge_adj_tiles.add(adj_tile)

        while edge_adj_tiles:
            tile = edge_adj_tiles.pop()
            q = [tile]
            if self._tile_is_inside(tile):
                # All adjacent tiles must also be inside...
                while q:
                    tile = q.pop()
                    x, y = tile
                    edge_adj_tiles.discard(tile)
                    for dx, dy in adjacents:
                        adj_tile = (x + dx, y + dy)
                        if adj_tile in edge_adj_tiles:
                            q.append(adj_tile)
            else:
                # all adjacent tiles must also be outside...
                while q:
                    tile = q.pop()
                    x, y = tile
                    self._out.add(tile)
                    edge_adj_tiles.discard(tile)
                    for dx, dy in adjacents:
                        adj_tile = (x + dx, y + dy)
                        if adj_tile in edge_adj_tiles and adj_tile not in self._out:
                            q.append(adj_tile)
    
    def add_x_edge_tile(self, tile):
        self._x_edge.add(tile)
        self._edge.add(tile)
    
    def add_y_edge_tile(self, tile):
        self._y_edge.add(tile)
        self._edge.add(tile)
    
    def _tile_is_inside(self, tile):
        if tile in self._edge:
            return True
        if tile in self._out:
            return False
        
        # Else, we need to count how many x or y edges it crosses traversing to a known out tile or boundary.
        # x and y range boundaries are 0/100000 by inspection.
        # An even number of crossings to out is outside the shape, an odd number is inside the shape. 
        # Not going to bother optimizing for traversing in other direction
        x, y = tile
        count = 0
        if x < y:
            # x is small, traverse across x edges.
            for x_i in range(x, -1, -1):
                if (x_i, y) in self._x_edge:
                    count += 1
                if (x_i, y) in self._out:
                    break
        else:
            for y_i in range(y, -1, -1):
                if (x, y_i) in self._y_edge:
                    count += 1
                if (x, y_i) in self._out:
                    break
        
        return count % 2 == 1
    
    def check_rectangle(self, tile_0, tile_1):
        """
        Traverse the rectangle edge in a spiral pattern and check if tiles are inside.
        I assume that there are no weird inclusions, which would require checking rectangle interiors.
        """
        x0, y0 = tile_0
        x1, y1 = tile_1
        x_min, x_max = (x0, x1) if x0 < x1 else (x1, x0)
        y_min, y_max = (y0, y1) if y0 < y1 else (y1, y0)
        
        # Check the opposite corners first.
        if not self._tile_is_inside((x0, y1)) or not self._tile_is_inside((x1, y0)):
            return False
                
        # Traverse rectangle boundary and see if it hits any out tiles.
        # This would not work if there are inclusions inside the shape...
        # traverse from x_min to x_max at y_min
        for x in range(x_min, x_max + 1):
            if (x, y_min) in self._out:
                return False
        y_min += 1
        if y_min == y_max: return True

        # from y_min + 1 to y_max at x_max
        for y in range(y_min, y_max + 1):
            if (x_max, y) in self._out:
                return False
        x_max -= 1
        if x_min == x_max: return True

        # x_min to x_max - 1 at y_max 
        for x in range(x_min, x_max + 1):
            if (x, y_max) in self._out:
                return False
        y_max -= 1
        if y_min == y_max: return True
        
        for y in range(y_min, y_max + 1):
            if (x_min, y) in self._out:
                return False
        x_min += 1
        if x_min == x_max: return True
        return True


class TimePrinter:
    def __init__(self):
        self._start_time = time.perf_counter()

    def print(self, msg, r = False):
        elapsed_time = time.perf_counter() - self._start_time
        if r:
            print(f"\r{elapsed_time:05.1f}s: \t{msg}", flush=True)
        else:
            print(f"{elapsed_time:05.1f}s: \t{msg}")


def edge_range(n0, n1):
    """Returns a range object which traverses from n1 to n2 inclusive"""
    small_n, big_n = (n0, n1) if n0 < n1 else (n1, n0)
    return range(small_n, big_n + 1)


if __name__ == "__main__":
    timer = TimePrinter()
    print("AoC Day 09.")
    input_file = input_arg_parse()
    lines = get_lines(input_file)
    
    red_tiles = [tuple(int(num) for num in tile.split(sep=',')) for tile in lines]
    
    rectangle_heap = []
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            heappush(rectangle_heap, (-((abs(x1 - x2) + 1) * (abs(y1 - y2)+1)), red_tiles[i], red_tiles[j]))   
            # Negative values to turn min heap into max
            # Area is inclusive of tiles.
    
    ans1 = -rectangle_heap[0][0]    # Don't pop it yet.
    timer.print(f"Part 1: {ans1}")
    
    # Build a grid set for part 2
    grid = GridSet()

    timer.print("Processing edges...")
    # Make a set which includes all the edge tiles.
    for i in range(0, len(red_tiles)):
        x0, y0 = red_tiles[i - 1]
        x1, y1 = red_tiles[i]
        
        if x0 == x1:    # x edge, because y changes
            for y in edge_range(y0, y1):
                grid.add_x_edge_tile((x0, y))
        elif y0 == y1:
            for x in edge_range(x0, x1):
                grid.add_y_edge_tile((x, y0))
    grid.process_edges()
    timer.print("Edges processed.")

    n = 0
    while rectangle_heap:
        area, tile_0, tile_1 = heappop(rectangle_heap)
        n += 1
        if n % 1000 == 0:
            timer.print(f"Checked {n} rectangles...", r=True)
        if grid.check_rectangle(tile_0, tile_1):
            timer.print(f"Part 2: {-area}")
            break
