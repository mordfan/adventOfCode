#!/bin/python3
# https://adventofcode.com/2025/day/9#part2

from os import path
from collections.abc import Iterator


def get_tiles(file_name: str) -> Iterator[tuple[int, int]]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            yield tuple(map(int, line.split(',')))


def main(file_name: str) -> None:
    points: dict[int, tuple[int, int]] = {i: t for i, t in enumerate(get_tiles(file_name))}

    lines: list[tuple[int, int, int, int]] = []  # [x1, y1, x2, y2]

    for p in range(1, len(points)):
        lines.append((
            points[p - 1][0],
            points[p - 1][1],
            points[p - 0][0],
            points[p - 0][1]
        ))

    # for l1 in range(lines(lines)):
    #     for l2 in range(l1 + 1, len(lines)):

    bestS = -1
    bestT = -1
    bestF = -1
    for s in points.keys():
        for t in range(s + 1, len(points)):
            x1 = min(points[s][0], points[t][0])
            x2 = max(points[s][0], points[t][0])
            y1 = min(points[s][1], points[t][1])
            y2 = max(points[s][1], points[t][1])

            field = (x2 - x1 + 1) * (y2 - y1 + 1)
            if field < bestF:
                continue

            corners = [
                (x1, y1),
                (x2, y1),
                (x1, y2),
                (x2, y2)
            ]
            ok = True
            for x in range(len(points)):
                if x == s or x == t:
                    continue

                if points[x] in corners:
                    continue

                if x1 < points[x][0] < x2 and \
                   y1 < points[x][1] < y2:
                    ok = False
                    break

            if not ok:
                continue

            if field > bestF:
                bestF = field
                bestS = s
                bestT = t

    print(f'best={points[bestS]}-{points[bestT]}, size{bestF:,}')


if __name__ == "__main__":
    main('example.txt')
    # main('input.txt')
