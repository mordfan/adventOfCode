#!/bin/python3
# https://adventofcode.com/2025/day/6#part2

from os import path
from collections.abc import Iterator
from functools import reduce


def get_data(file_name: str) -> Iterator[tuple[list[int], str]]:
    lines: list[str] = []
    with open(path.join('data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline()):
            lines.append(line.replace('\n', ' '))

    splitters: list[int] = []
    i = max(map(len, lines))
    splitters.append(i)
    while i > 0:
        i = len(lines[-1][:i].rstrip()) - 1
        splitters.append(i)

    for s in range(1, len(splitters)):
        op = lines[-1][splitters[s]]
        text = [line[splitters[s]: splitters[s - 1] - 1] for line in lines[:-1]]
        numbers = list([int(''.join(x)) for x in zip(*text)])
        # print(f"{text=}")
        # print(f"{numbers=}")
        # print(f"{op=}")
        # print("===")
        yield (numbers, op)


def main(file_name: str) -> None:
    total: int = 0
    for (numbers, op) in get_data(file_name):
        if op == '*':
            total += reduce((lambda x, y: x * y), numbers)
        elif op == '+':
            total += sum(numbers)
        else:
            raise NotImplementedError("Unsupported op={ops[o]}")

    print(f"{total=:,}")


if __name__ == '__main__':
    main('example.txt')
    # main('input.txt')
