#!/bin/python3
# https://adventofcode.com/2025/day/5

from os import path


def get_ingredients(file_name: str) -> tuple[list[tuple[int, int]], list[int]]:
    fresh: list[tuple[int, int]] = []
    avail: list[int] = []
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline()):
            if len(line) <= 1:
                continue
            si = line.find('-')
            if si < 0:
                avail.append(int(line.rstrip()))
            else:
                fresh.append((int(line[:si]), int(line[si+1:])))
    return (fresh, avail)


def main(file_name: str) -> None:
    (fresh_ranges, avail) = get_ingredients(file_name)
    # double list comprehension gets You killed! xD
    # fresh_distinct: set[int] = set([x for (first, last) in fresh_ranges for x in range(first, last + 1)])
    # fresh_counter: int = sum(1 if x in fresh_distinct else 0 for x in avail)

    fresh_counter: int = 0
    for a in avail:
        for (first, last) in fresh_ranges:
            if first <= a <= last:
                fresh_counter += 1
                break

    print(f"{fresh_counter=}")


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
