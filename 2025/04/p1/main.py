#!/bin/python3
# https://adventofcode.com/2025/day/4

from os import path
from collections.abc import Iterator


def read_grid_from_file(file_name: str) -> Iterator[str]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8', newline='\n') as file:
        while (line := file.readline()):
            yield line.strip()


def get_grid(file_name: str) -> list[str]:
    ret: list[str] = []
    for line in read_grid_from_file(file_name):
        ret.append(f'.{line}.')
    ret.insert(0, '.' * (len(ret[0])))
    ret.append('.' * (len(ret[0])))
    return ret


def main(file_name: str) -> None:
    grid = get_grid(file_name)
    coords: list[tuple[int, int]] = []  # list of (x, y) that have less then 4 rolls around
    neighbors: list[(int, int)] = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[r]) - 1):
            if grid[r][c] != '@':
                continue
            if sum([(1 if grid[r + nr][c + nc] == '@' else 0) for (nr, nc) in neighbors]) >= 4:
                continue
            coords.append((r - 1, c - 1))

    print(f"Number of rolls to move = {len(coords)}")
    return
    print(grid)
    for (r, c) in coords:
        print(r, c)


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
