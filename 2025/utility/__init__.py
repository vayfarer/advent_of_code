import path
import sys
import time


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
    with open(file_path, "r") as f:
        out = f.read().splitlines()
    return out


class TimePrinter:
    def __init__(self):
        self._start_time = time.perf_counter()

    def print(self, msg, r = False):
        elapsed_time = time.perf_counter() - self._start_time
        if r:
            print(f"\r{elapsed_time:05.1f}s: \t{msg}", flush=True)
        else:
            print(f"{elapsed_time:05.1}s: \t{msg}")