from utility import get_lines, input_arg_parse


if __name__ == "__main__":
    print("AoC Day 06.")
    input_file = input_arg_parse()
    lines = get_lines(input_file)
    
    starting_tachyon_idx = lines[0].index("S")
    
    ans1 = 0
    tachyon_dict = {starting_tachyon_idx: 1}    # dict values are # of timelines.
    for line_idx in range(2, len(lines), 2):    # Input data only has splits on even index lines.
        for i in list(tachyon_dict.keys()): # Need to make list of keys b/c dict must not change size during for loop.
            if lines[line_idx][i] == "^":   # split!
                ans1 += 1
                timelines = tachyon_dict.pop(i)
                if i - 1 >= 0:  # Index range checks not strictly necessary with given inputs. 
                    tachyon_dict[i - 1] = tachyon_dict.get(i - 1, 0) + timelines
                if i + 1 < len(lines[0]):
                    tachyon_dict[i + 1] = tachyon_dict.get(i + 1, 0) + timelines
    print(f"Part 1: {ans1}")
    
    ans2 = sum(tachyon_dict.values())
    print(f"Part 2: {ans2}")
