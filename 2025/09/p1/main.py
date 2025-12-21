#!/bin/python3
# https://adventofcode.com/2025/day/9

from os import path
from collections.abc import Iterator


def read_tiles(file_name: str) -> Iterator[tuple[int, int]]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            yield tuple(map(int, line.split(',')))


def main(file_name: str) -> None:
    xMax, yMax = 0, 0
    tiles: list[tuple[int, int]] = []
    for x, y in read_tiles(file_name):
        tiles.append((x, y))
        if x > xMax:
            xMax = x
        if y > yMax:
            yMax = y

    bestS = (0, 0)
    bestT = (0, 0)
    bestF = 0
    for i, s in enumerate(tiles):
        for t in tiles[:i + 1]:
            field = (abs(t[0] - s[0]) + 1) * (abs(t[1] - s[1]) + 1)
            if field > bestF:
                bestF = field
                bestS = s
                bestT = t

    print(f'{bestS=}, {bestT=}, {bestF=:,}')


if __name__ == "__main__":
    # main('example.txt')
    main('input.txt')
