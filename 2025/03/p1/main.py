#!/bin/python3
# https://adventofcode.com/2025/day/3

from os import path
from collections.abc import Iterator


def read_input(file_name: str) -> Iterator[str]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            if not line:
                break
            yield line.strip()


def get_max_joltage(bank: str) -> tuple[int, int, int]:
    a: int = 0
    b: int = 0
    for i in range(1, len(bank) - 1):
        if bank[i] > bank[a]:
            a = i
        if bank[i] == '9':
            break
    b = a + 1
    for i in range(a + 1, len(bank)):
        if bank[i] > bank[b]:
            b = i
        if bank[i] == '9':
            break

    return (int(bank[a] + bank[b]), a, b)


def main(file_name: str) -> None:
    s: int = 0
    for bank in read_input(file_name):
        (j, a, b) = get_max_joltage(bank)
        print(f'bank: "{bank}" = {j} ({a} + {b})')
        s += j
        # break
    print(f"total joltage: {s}")


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
