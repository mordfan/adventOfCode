#!/bin/python3
# https://adventofcode.com/2025/day/3#part2

from os import path
from collections.abc import Iterator


def read_input(file_name: str) -> Iterator[str]:
    with open(path.join('data', file_name), mode='r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            if not line:
                break
            yield line.strip()


def get_max_joltage(bank: str, num: int) -> tuple[int, list[int]]:
    """Returns joltage and list of turned on battery indices"""

    a: int = 0
    indices: list[int] = []
    for b in range(num):
        bMax = len(bank) - num + b + 1
        # print(f"{a=}, {b=} / {bMax=}")
        for i in range(a, bMax):
            if bank[i] > bank[a]:
                a = i
            if bank[i] == '9':
                indices.append(a)
                a += 1
                break
        else:
            indices.append(a)
            a += 1

    jolts = int(''.join([bank[i] for i in indices]))
    return (jolts, indices)


def main(file_name: str, num: int) -> None:
    s: int = 0
    for bank in read_input(file_name):
        (j, indices) = get_max_joltage(bank, num)
        s += j
        # print(f'bank: "{bank}" = {j}')
        # print(f'used: [{("".join(["^" if i in indices else " " for i in range(len(bank))]))}]')
    print(f"total joltage: {s}")


if __name__ == '__main__':
    # main('example.txt', 2)
    # main('example.txt', 12)
    main('input.txt', 12)
