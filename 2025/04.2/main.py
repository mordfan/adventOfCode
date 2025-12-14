#!/bin/python3
from collections.abc import Iterator


def read_grid_from_file(file_name: str) -> Iterator[str]:
    with open(file_name, mode='r', encoding='utf-8', newline='\n') as file:
        while (line := file.readline()):
            yield line.strip()


def get_grid(file_name: str) -> list[list[str]]:
    ret: list[list[str]] = []
    for line in read_grid_from_file(file_name):
        ret.append(list(line))
        ret[-1].insert(0, '.')
        ret[-1].append('.')
    ret.insert(0, list('.' * len(ret[0])))
    ret.append(list('.' * len(ret[0])))
    return ret


def main(file_name: str) -> None:
    grid = get_grid(file_name)

    coords: list[tuple[int, int]] = []  # list of (x, y) that have less then 4 rolls around
    neighbors: list[(int, int)] = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    total: int = 0
    round: int = 0
    while True:
        round += 1
        for r in range(1, len(grid) - 1):
            for c in range(1, len(grid[r]) - 1):
                if grid[r][c] != '@':
                    continue
                if sum([(1 if grid[r + nr][c + nc] == '@' else 0) for (nr, nc) in neighbors]) >= 4:
                    continue
                coords.append((r, c))

        print(f"{round=}, Number of rolls to move = {len(coords)}")
        if len(coords) == 0:
            break

        total += len(coords)

        for (r, c) in coords:
            grid[r][c] = '.'
        coords.clear()

    print(f"Total number of rolls moved = {total} after {round} rounds")


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
