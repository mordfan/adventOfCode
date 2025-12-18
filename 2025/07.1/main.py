#!/bin/python3
# https://adventofcode.com/2025/day/7

from os import path
from collections.abc import Iterator


def get_data(file_name: str) -> Iterator[str]:
    with open(path.join('data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            yield line


def main(file_name: str) -> None:
    total: int = 0
    beams: set[int] = set()
    lines_iterator = get_data(file_name)
    line = next(lines_iterator)
    beams.add(line.find('S'))
    assert len(beams) == 1, "Invalid number of starting points!"
    # print(beams)
    for line in lines_iterator:
        # print(f"before={line}")
        splitters = list([i for i, x in enumerate(list(line)) if x == "^"])
        if not splitters:
            continue
        # print(splitters)
        for s in splitters:
            if s in beams:
                total += 1
                beams.remove(s)
                beams.update([s - 1, s + 1])

    pass

    print(f"{beams=}")
    print(f"total number of splits={total:,}")


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
