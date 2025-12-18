#!/bin/python3
# https://adventofcode.com/2025/day/2

from os import path
from collections.abc import Iterator


def get_ranges(file_name: str) -> Iterator[tuple[int, int]]:
    data: str = ''
    with open(path.join('data', file_name), mode='r', encoding='utf-8') as file:
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
    for i in range(start, stop + 1):
        idStr = str(i)
        idLen = len(idStr)
        if idLen % 2 != 0:
            continue
        midLen = int(idLen / 2)
        if all([idStr[c] == idStr[midLen + c] for c in range(midLen)]):
            # print(f"\t{idStr}")
            yield i


def main(file_name: str) -> None:
    s: int = 0
    for (start, stop) in get_ranges(file_name):
        # print(f"{start}-{stop} ")
        for i in get_invalid_ids(start, stop):
            s += i

    print(f"{s=}")

if __name__ == '__main__':
    main('example.txt')
    main('input.txt')
