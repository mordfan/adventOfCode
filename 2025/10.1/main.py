#!/bin/python3
# https://adventofcode.com/2025/day/10
from collections.abc import Iterator


def get_data(file_name: str) -> Iterator[tuple[list[bool], list[list[int], list[int]]]]:
    with open(file_name, mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            assert line.startswith('['), "invalid begining of line"

            # light diagram
            b = 0
            e = line.find(']', b)
            assert e > b, "could not locate light diagram"
            ld = [True if c == '#' else False for c in line[b + 1:e]]

            # button wirings
            b = e + 1
            e = line.find('{', b)
            assert e > b, "could not locate button wiring"
            bw = [list(map(int, x.split(','))) for x in line[b + 1: e - 2].lstrip('(').rstrip(')').split(') (')]

            # joltage requirements
            b = e + 1
            e = line.find('}', b)
            assert e > b, "could not locate joltage requirements"
            jr: list[int] = list(map(int, line[b:e].split(',')))

            yield (ld, bw, jr)


def main(file_name: str) -> None:
    for ld, bw, jr in get_data(file_name):
        print(f'---\n{ld=}\n{bw=}\n{jr=}')
        continue


if __name__ == "__main__":
    main('example.txt')
    # main('input.txt')
