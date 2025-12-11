from utility import get_lines, input_arg_parse, TimePrinter
import re
from scipy import optimize


def min_buttons(indicator_lights, buttons, light_state:tuple = None, n_pushed: int = 0):
    """
    DFS.
    """
    if light_state is None:
        light_state = tuple(False for _ in range(len(indicator_lights)))

    # Check not flipping a switch.
    if light_state == indicator_lights:
        return n_pushed

    # Check flipping the first switch.
    new_light_state = tuple(light_state[i] if i not in buttons[0] else not light_state[i] for i in range(len(indicator_lights)))
    if new_light_state == indicator_lights:
        return n_pushed + 1

    # Check subsequent switches.
    if len(buttons) > 1:
        rem_buttons = buttons[1:]
        return min(min_buttons(indicator_lights, rem_buttons, light_state, n_pushed), min_buttons(indicator_lights, rem_buttons, new_light_state, n_pushed + 1))

    # No switches left.
    return len(indicator_lights) + 1


if __name__ == "__main__":
    timer = TimePrinter()
    print("AoC Day 10.")
    input_file = input_arg_parse()
    lines = get_lines(input_file)

    machines = []

    for line in lines:
        line_parts = line.split(sep = ' ')

        indicator_lights = tuple('#' == symbol for symbol in re.findall(r"([.#])", line_parts[0]))
        buttons = tuple(set(int(n) for n in re.findall(r"([0-9]+)", button)) for button in line_parts[1:-1])
        joltage_requirements = tuple(int(n) for n in re.findall(r"([0-9]{1,})", line_parts[-1]))

        machines.append((indicator_lights, buttons, joltage_requirements))

    ans1 = 0
    for indicator_lights, buttons, _ in machines:
        ans1 += min_buttons(indicator_lights, buttons)
    timer.print(f"Part 1: {ans1}")

    ans2 = 0
    for _, buttons, joltage_requirements in machines:
        c = [1] * len(buttons)
        button_array = [[1 if i in button else 0 for button in buttons] for i in range(len(joltage_requirements))]
        ans2 += sum(optimize.linprog(c=c, A_eq=button_array, b_eq=joltage_requirements, integrality=c).x)
    timer.print(f"Part 2: {ans2}")
