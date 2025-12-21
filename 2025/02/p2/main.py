#!/bin/python3
# https://adventofcode.com/2025/day/2#part2

from os import path
from collections.abc import Iterator


DIVISORS: dict[int, list[int]] = {
        2: [1],
        3: [1],
        4: [1, 2],
        5: [1],
        6: [1, 2, 3]
    }


def get_divisors(idLen: int) -> list[int]:
    if idLen < 2:
        return []
    if idLen not in DIVISORS.keys():
        DIVISORS[idLen] = [1]
        for i in range(2, int(idLen/2) + 1):
            if idLen % i != 0:
                continue
            DIVISORS[idLen].append(i)
    return DIVISORS[idLen]


def get_ranges(file_name: str) -> Iterator[tuple[int, int]]:
    data: str = ''
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        data = file.read().strip()

    start: int = 0
    stop: int = 0
    separator: int = 0
    while True:
        i = data.find(',', start)
        stop = i if i >= 0 else len(data)
        separator = data.find('-', start, stop)
        assert separator > 0, "no separator found!"
        yield (int(data[start:separator]), int(data[separator + 1:stop]))
        if i < 0:
            return
        start = stop + 1


def get_invalid_ids(start: int, stop: int) -> Iterator[int]:
    for number in range(start, stop + 1):
        # print(f"\t{number=}")
        s = str(number)
        for divisor in get_divisors(len(s)):
            parts = list(map(''.join, zip(*[iter(s)]*divisor)))
            isValid = len(set(parts)) > 1
            if number == 99998:
                print(f"\t\t{divisor=}, {isValid=}, {parts=}")
            if not isValid:
                yield number
                break


def main(file_name: str) -> None:
    s: int = 0
    for (start, stop) in get_ranges(file_name):
        print(f"{start}-{stop} ")
        for m in get_invalid_ids(start, stop):
            print(f"\t\t{m=}")
            s += m
    print(f"{s=}")


if __name__ == '__main__':
    # print(get_divisors(len(str(262626))))
    # main('example.txt')
    main('input.txt')
