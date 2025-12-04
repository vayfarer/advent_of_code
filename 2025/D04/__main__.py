from utility import get_lines, input_arg_parse


def remove_rolls(rolls_dict):
    """
    rolls_dict is map of rolls indexed by (m, n) tuples of roll positions.
    Returns the number of rolls which can and are removed.
    Updates rolls_dict in place.
    """

    def grid_adjacents(m, n):
        adj_out = []
        adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dm, dn in adjacents:
            new_m = m + dm
            new_n = n + dn
            if (new_m, new_n) in rolls_dict:
                adj_out.append((new_m, new_n))
        return adj_out

    for roll in rolls_dict:
        for adj_roll in grid_adjacents(*roll):
            rolls_dict[adj_roll] += 1

    removed_rolls = []
    for roll in rolls_dict:
        if rolls_dict[roll] < 4:
            removed_rolls.append(roll)
        else:
            rolls_dict[roll] = 0

    for roll in removed_rolls:
        rolls_dict.pop(roll)

    return len(removed_rolls)


if __name__ == "__main__":
    print("AoC Day 04.")
    input_file = input_arg_parse()
    rolls_lines = get_lines(input_file)

    rolls_dict = {}
    for m, line in enumerate(rolls_lines):
        for n, char in enumerate(line):
            if char == '@':
                rolls_dict[(m, n)] = 0
    original_rolls = len(rolls_dict)
    remove_rolls(rolls_dict)

    ans1 = original_rolls - len(rolls_dict)
    print(f"Part 1: {ans1}")

    while remove_rolls(rolls_dict):
        pass
    ans2 = original_rolls - len(rolls_dict)
    print(f"Part 2: {ans2}")
