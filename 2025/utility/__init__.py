import path
import sys


def input_arg_parse():
    # setting path for reading input files
    module_path = sys.argv[0]
    directory = path.Path(module_path).parent
    sample_input = directory / "sample_input"
    problem_input = directory / "input"

    if len(sys.argv) == 2:
        if '-sample' in sys.argv:
            return sample_input
        else:
            print(f"'{sys.argv[1]}' not recognized.")
    elif len(sys.argv) > 2:
        print("Too many arguments. Use: python -m [module] [-sample]")
    return problem_input


def get_lines(file_path):
    """Read input file. Outputs a list of stripped strings."""
    out = []
    with open(file_path) as f:
        line = f.readline().strip()
        while line:
            out.append(line)
            line = f.readline().strip()
    return out