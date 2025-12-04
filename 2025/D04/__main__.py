import path
import sys


def input_arg_parse():
    # setting path for reading input files
    directory = path.Path(__file__).parent
    sample_input = directory / "sample_input"
    problem_input = directory / "input"

    if len(sys.argv) == 2:
        if '-sample' in sys.argv:
            return sample_input
        else:
            print(f"'{sys.argv[1]}' not recognized.")
    elif len(sys.argv) > 2:
        print("Too many arguments. Use: python D03 [-sample]")
    return problem_input



if __name__ == "__main__":
    print("AoC Day 04.")