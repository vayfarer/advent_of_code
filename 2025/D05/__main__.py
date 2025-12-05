from utility import get_lines, input_arg_parse


if __name__ == "__main__":
    print("AoC Day 05.")
    input_file = input_arg_parse()
    combo_lines = get_lines(input_file)

    split = combo_lines.index('')
    id_range_strings = combo_lines[0:split]
    ingreds = [int(n) for n in combo_lines[split + 1:]]
    ingreds.sort()

    id_ranges = []
    for id_range in id_range_strings:
        id_strings = id_range.split(sep='-')
        id_ranges.append((int(id_strings[0]), int(id_strings[1])))

    # Sort and concatenate ranges.
    id_ranges.sort()
    temp_id_ranges = []
    for id_range in id_ranges:
        if temp_id_ranges:
            prev_range = temp_id_ranges[-1]
            if id_range[0] <= prev_range [1]:
                # merge and continue.
                temp_id_ranges[-1] = (prev_range[0], max(id_range[1], prev_range[1]))
                continue
        temp_id_ranges.append(id_range)
    id_ranges = temp_id_ranges

    # Count part 1.
    ans1 = 0
    id_idx = 0
    for ingred in ingreds:
        if ingred < id_ranges[id_idx][0]:
            continue

        while id_idx < len(id_ranges) and ingred > id_ranges[id_idx][1]:
            id_idx += 1

        if id_idx >= len(id_ranges):
            break

        if id_ranges[id_idx][0] <= ingred <= id_ranges[id_idx][1]:
            ans1 += 1
    print(f"Part 1: {ans1}")

    # Calc part 2.
    ans2 = 0
    for min_id, max_id in id_ranges:
        ans2 += max_id - min_id + 1
    print(f"Part 2: {ans2}")



