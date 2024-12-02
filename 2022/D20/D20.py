# Advent of Code 2022, Day 20 Part 1 and 2
# Michael Chen
# 12/30/2022

class EnumListException(Exception):
    pass

class EnumList:
    def __init__(self, seq:list):
        """A list data structure which associates an index with the value.
        The size of the EnumList should not change."""
        self._data = [[value, i] for i, value in enumerate(seq)]
        self._size = len(seq)

    def move(self, cur_index:int, new_index:int):
        """Moves a value from current index to new index"""

        if cur_index > self._size or cur_index < 0 or new_index > self._size or new_index < 0:
            raise EnumListException(f"Index out of domain. cur_index: {cur_index}, new_index: {new_index}, size: {self._size}")

        if cur_index == new_index:
            return

        if cur_index < new_index:
            ran = range(cur_index, new_index)
        else:
            ran = range(cur_index, new_index, -1)

        moved_val = self._data.pop(cur_index)
        self._data.insert(new_index, moved_val)

        for i in ran:
            self._data[i][1] = i

        self._data[new_index][1] = new_index

    def __str__(self):
        out = '['
        for num in self._data:
            out += str(num[0]) + ', '
        out += ']'
        return out

    def __iter__(self):
        """Create iterator for loop. """
        self._index = 0
        return self

    def __next__(self):
        """Obtain next value and advance iterator. """
        try:
            value = self[self._index]
        except EnumListException:
            raise StopIteration

        self._index += 1
        return value

    def __getitem__(self, index: int):
        """Enable bracketed indexing. Return value from given index position.
        """
        if index < 0 or index >= self._size:
            raise EnumListException('Index out of bounds')
        return self._data[index]

    def __setitem__(self, index: int, value: list) -> None:
        """Enable bracketed indexing. Store value at given index in the array.
        """
        if index < 0 or index >= self._size:
            raise EnumListException('Index out of bounds')
        self._data[index] = value

    def __len__(self) -> int:
        """Return length of the enumlist (number of elements)."""
        return self._size

def elf_decrypt(numbers:list, key_d:int=1, cycles:int=1):
    """Decryption according to the problem statement."""

    len_seq = len(numbers)
    numbers = [n * key_d for n in numbers]

    sequence = EnumList(numbers)
    sequence_outer = []

    for i in range(len_seq):
        # Did not use list comprehension in order to find the zero in loop.
        sequence_outer.append(sequence[i])
        if sequence[i][0] == 0:
            zero = sequence[i]

    for _ in range(cycles):
        for number_i in sequence_outer:
            sequence.move(number_i[1], (number_i[1]+number_i[0]) % (len_seq -1))

    coordinate_sum = 0
    for i in range(1,4):
        # Assumption from problem statement: there is always a zero to be found.
        index = i * 1000 + zero[1]
        index %= len_seq
        coordinate_sum += sequence[index][0]

    return coordinate_sum


if __name__ == "__main__":

    key_d = 811589153
    cycles_d = 10

    with open('input.txt') as f:
        input1 = f.read().strip()
    lines = input1.split('\n')
    numbers = [int(number) for number in lines]

    print(f'Part 1: {elf_decrypt(numbers)}')
    print(f'Part 2: {elf_decrypt(numbers, key_d, cycles_d)}')





