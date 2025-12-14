#!/bin/python3
# https://adventofcode.com/2025/day/6
from functools import reduce


def get_data(file_name: str) -> tuple[list[list[int]], list[str]]:
    data: list[list[str]] = []
    with open(file_name, mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            data.append(line.split())
    numbers: list[list[int]] = [list(map(int, y)) for y in zip(*data[:-1])]
    ops: list[str] = data[-1]
    return (numbers, ops)


def main(file_name: str) -> None:
    numbers, ops = get_data(file_name)
    total: int = 0
    for o in range(len(ops)):
        if ops[o] == '*':
            total += reduce((lambda x, y: x * y), numbers[o])
        elif ops[o] == '+':
            total += sum(numbers[o])
        else:
            raise NotImplementedError("Unsupported op={ops[o]}")

    print(f"{total=:,}")


if __name__ == '__main__':
    main('example.txt')
    # main('input.txt')
