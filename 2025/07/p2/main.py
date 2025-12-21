#!/bin/python3
# https://adventofcode.com/2025/day/7#part2

from os import path
from collections.abc import Iterator


def get_data(file_name: str) -> Iterator[str]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            yield line


def main(file_name: str) -> None:
    lines_iterator = get_data(file_name)
    line = next(lines_iterator)
    firstBeam: int = line.find('S')
    beams: set[int] = set([firstBeam])
    counters: dict[int, int] = {i: 0 for i in range(len(line))}
    counters[firstBeam] = 1
    print(''.join([str(counters[i]) if counters[i] > 0 else '.' for i in range(len(line))]))
    for line in lines_iterator:
        splitters = list([i for i, l in enumerate(list(line)) if l == '^'])
        if not splitters:
            print(''.join(['|' if i in beams else '^' if i in splitters else '.' for i in range(len(line))]))
            continue

        for s in splitters:
            if s not in beams:
                continue
            beams.remove(s)
            beams.update([s - 1, s + 1])

        for b in beams:
            if b - 1 in splitters:
                counters[b] += counters[b - 1]
            if b + 1 in splitters:
                counters[b] += counters[b + 1]

        for s in splitters:
            counters[s] = 0

        print(''.join([str(counters[i])[0] if counters[i] > 0 else '.' for i in range(len(line))]), sum(counters.values()))
        print(''.join(['|' if i in beams else '^' if i in splitters else '.' for i in range(len(line))]))

    print(f'total number of worlds={sum(counters.values()):,}')


if __name__ == '__main__':
    main('example.txt')
    # main('input.txt')
