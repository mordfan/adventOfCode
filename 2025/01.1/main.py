#!/bin/python
# https://adventofcode.com/2025/day/1

from collections.abc import Iterator


def get_sequence(file_name: str) -> Iterator[tuple[str, int]]:
    """Returns tuple(direction, clicks)"""
    with open(file_name, mode='r', encoding='utf-8') as file:
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
    print(f'current_position is {current_position}')

    for (direction, clicks) in get_sequence(input_file_name):
        if direction == 'L':
            current_position -= clicks
            while current_position < 0:
                current_position += 100
        elif direction == 'R':
            current_position += clicks
            while current_position >= 100:
                current_position -= 100

        if current_position == 0:
            password += 1

        print(f'{clicks:>5} {direction} -> {current_position:>2} {(" <" if current_position == 0 else "")}')

    print(f'password is {password}')


if __name__ == '__main__':
    # main('example.txt', 50)
    main('input.txt', 50)
