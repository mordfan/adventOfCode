#!/bin/python3
# https://adventofcode.com/2025/day/8

from collections.abc import Iterator
from math import pow, sqrt
from heapq import heapify, heappush, heappop
from functools import reduce

def get_junction_boxes(file_name: str) -> Iterator[tuple[int, int, int]]:
    with open(file_name, mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            x, y, z, *_ = map(int, line.split(',', maxsplit=4))
            yield (x, y, z)


def get_distance(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> float:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    d = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2) + pow((z2 - z1), 2))
    return d


def main(file_name: str) -> None:
    boxes: dict[int, tuple[int, int, int]] = dict(enumerate(get_junction_boxes(file_name)))
    circuits: dict[int, int] = {x: -1 for x in boxes.keys()}  # bc[boxId] = circuitId
    distances: list[tuple[int, int]: float] = []
    heapify(distances)

    for x in boxes.keys():
        for y in range(x + 1, len(boxes)):
            d = get_distance(boxes[x], boxes[y])
            heappush(distances, (d, (x, y)))

    print("start")
    currentCircuitId: int = -1
    lastX: int
    lastY: int
    while distances:
        d, (x, y) = heappop(distances)

        # print(f'\n{c=}, {x=}, {y=}, {boxes[x]}-{boxes[y]}={d}')

        if circuits[x] >= 0 and circuits[y] >= 0:
            if circuits[x] == circuits[y]:
                # print('= X and Y belongs to the same curcuit')
                continue
            # print(f'> joining {circuits[x]} and {circuits[y]}')
            lastX = x
            lastY = y
            oldId = circuits[y]
            newId = circuits[x]
            for k, v in circuits.items():
                if v != oldId:
                    continue
                circuits[k] = newId
            continue

        if circuits[x] < 0 and circuits[y] < 0:
            currentCircuitId += 1
            # print(f'* new circuit (id={currentCircuitId})')
            circuits[x] = currentCircuitId
            circuits[y] = currentCircuitId
            lastX = x
            lastY = y
        elif circuits[x] < 0:
            # print(f'+ X assigned to {circuits[y]}')
            circuits[x] = circuits[y]
            lastX = x
            lastY = y
        elif circuits[y] < 0:
            # print(f'+ Y assigned to {circuits[x]}')
            circuits[y] = circuits[x]
            lastX = x
            lastY = y

    print(f'x={boxes[lastX]}, y={boxes[lastY]}, x.x*y.x={(boxes[lastX][0] * boxes[lastY][0]):,}')


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
