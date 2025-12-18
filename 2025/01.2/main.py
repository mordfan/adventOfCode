#!/bin/python3
# https://adventofcode.com/2025/day/1#part2

from os import path
from collections.abc import Iterator


def get_sequence(file_name: str) -> Iterator[tuple[str, int]]:
    """Returns tuple(direction, clicks)"""
    with open(path.join('data', file_name), mode='r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            if not line:
                break

            entry = line.strip().upper()
            if not entry.startswith('L') and not entry.startswith('R'):
                assert False, 'Invalid entry!'

            yield (entry[0:1], int(entry[1:]))


def main(input_file_name: str, current_position: int) -> None:
    password: int = 0
    print(f'*** current_position is {current_position}')

    for (direction, clicks) in get_sequence(input_file_name):
        previous_position = current_position
        change: int = 0
        if clicks >= 100:
            change += (clicks // 100)
            clicks -= (change * 100)

        if direction == 'L':
            if current_position == 0:
                change -= 1
            current_position -= clicks
            if current_position < 0:
                current_position += 100
                change += 1
        elif direction == 'R':
            current_position += clicks
            if current_position > 100:
                change += 1
                current_position -= 100
            elif current_position == 100:
                current_position -= 100

        if current_position == 0:
            change += 1

        print(f'{direction}{clicks:<5}'
              f'{previous_position:>3}{"+" if direction == "R" else "-"}{clicks:<3}'
              f' -> '
              f'{current_position:>2} {format(change, "+0") if change else ""}')
        password += change

    print(f'*** password is {password}')


if __name__ == '__main__':
    # main('example.txt', 50)
    main('input.txt', 50)
