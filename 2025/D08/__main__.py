from heapq import heappush, heappop
from utility import get_lines, input_arg_parse
import sys


class Junctionator:
    def __init__(self, junctions: list):
        """junctions is list of junction coordinates in tuple form: (x, y, z)"""
        self._junctions = junctions
        
        # Calculate all junc-junc distances and insert into a min-heap.
        self._junc_distance_q = []
        for i in range(len(self._junctions)):
            for j in range(i + 1, len(self._junctions)):
                junc_i = self._junctions[i]
                junc_j = self._junctions[j]
                heappush(self._junc_distance_q, (sum([(junc_i[_] - junc_j[_]) ** 2 for _ in range(3)]), junc_i, junc_j))

        # Implement a two-way dictionary mapping.
        # Junction dictionary - each junction address may get one network id
        self._junc_net_dict = {}
        # Network dictionary - each network id may get a list of multiple junction address
        self._net_junc_dict = {}
        
        # tracks last operated net_id, which will be useful for part 2.
        self._last_net_id = None
    
    def connect_n(self, n):
        """Make n connections starting from the closest."""
        for _ in range(n):
            self._connect_shortest()
            
    def connect_until_1_net(self):
        """Make connections until all juncs are in one network."""
        if len(self._net_junc_dict) < 1:
            # This is not strictly necessary, I only run after connecting at least some in part 1.
            self._connect_shortest()
        
        junc_x1, junc_x2 = None, None
        while len(self._net_junc_dict[self._last_net_id]) != len(self._junctions):
            junc_x1, junc_x2 = self._connect_shortest()
        
        return junc_x1[0] * junc_x2[0]
        
    def _gen_net_id(self):
        num = 0
        while True:
            yield num
            num += 1
    
    def _connect_shortest(self):
        """
        Make a single connection, starting with the shortest available.
        Returns the coords of the junctions involved, which is useful for part 2.
        """
        distance, junc_1, junc_2 = heappop(self._junc_distance_q)
        # Check if either junc is in a network.
        net_1, net_2 = self._junc_net_dict.get(junc_1, None), self._junc_net_dict.get(junc_2, None)
        # If both are in networks, then merge the smaller network into the bigger network.
        if net_1 is not None and net_2 is not None:
            if net_1 == net_2:  # juncs are already in the same network.
                return junc_1, junc_2
            big_net, small_net = (net_1, net_2) if len(self._net_junc_dict[net_1]) >= len(self._net_junc_dict[net_2]) else (net_2, net_1)
            small_net_juncs = self._net_junc_dict.pop(small_net)
            for junc in small_net_juncs:
                self._junc_net_dict[junc] = big_net
            self._net_junc_dict[big_net].extend(small_net_juncs)
            self._last_net_id = big_net
        # One is in a network. Merge the other into the network.
        elif net_1 is not None or net_2 is not None:
            mother_net, orphan_junc = (net_1, junc_2) if net_1 is not None else (net_2, junc_1)
            self._net_junc_dict[mother_net].append(orphan_junc)
            self._junc_net_dict[orphan_junc] = mother_net
            self._last_net_id = mother_net
        # Neither is in a network. Assign both into one network.
        else:
            new_net_id = self._gen_net_id()
            self._junc_net_dict[junc_1], self._junc_net_dict[junc_2] = new_net_id, new_net_id
            self._net_junc_dict[new_net_id] = [junc_1, junc_2]
            self._last_net_id = new_net_id
        
        return junc_1, junc_2
                
    def big_3_nets_product(self):
        """Return the product of the length of the biggest 3 current networks."""
        big_3_nets = []
        for net in self._net_junc_dict.values():
            heappush(big_3_nets, len(net))
            if len(big_3_nets) > 3:
                heappop(big_3_nets)
                
        out = 1
        for n in big_3_nets:
            out *= n
        return out
        

if __name__ == "__main__":
    print("AoC Day 08.")
    input_file = input_arg_parse()
    lines = get_lines(input_file)
    
    junctions= [line.split(sep=',') for line in lines]
    junctions = [(int(j[0]), int(j[1]), int(j[2])) for j in junctions]    
    junctions = Junctionator(junctions)
    
    n = 10 if len(sys.argv) > 1 and sys.argv[1] == '-sample' else 1000
    junctions.connect_n(n)
    ans1 = junctions.big_3_nets_product()
    print(f"Part 1: {ans1}")
    
    ans2 = junctions.connect_until_1_net()
    print(f"Part 2: {ans2}")
    