#!/bin/python3
# https://adventofcode.com/2024/day/1


def get_lists_of_ids(file_name: str) -> tuple[list[int], list[int]]:
    l: list[int] = []
    r: list[int] = []

    with open(file_name, mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            spacer = line.find(' ')
            if spacer < 0:
                continue

            l.append(int(line[:spacer]))
            r.append(int(line[spacer+1:]))

    return (l, r)


def main(file_name: str) -> None:
    (l, r) = get_lists_of_ids(file_name)

    l.sort()
    r.sort()

    total: int = 0

    for i in range(len(l)):
        total += abs(l[i] - r[i])

    print(f"total distance = {total}")


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
