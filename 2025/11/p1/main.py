#!/bin/python3
# https://adventofcode.com/2025/day/11

from os import path
from collections.abc import Iterator


def get_data(file_name: str) -> Iterator[tuple[str, set[str]]]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            i = line.find(':')
            assert i > 0, "invalid input!"

            name = line[:i]
            outputs = set(line[i + 2:].split(' '))

            yield (name, outputs)


def main(file_name: str) -> None:
    connections: dict[str, set[str]] = {node: outputs for node, outputs in get_data(file_name)}
    results: list[list[str]] = []

    def traverse(node: str, current_path: list[str]) -> None:
        if node == "out":  # in case there is no further path
            current_path.append(node)
            results.append(current_path.copy())
            return

        current_path.append(node)
        for child in connections[node]:  # else traverse further
            traverse(child, current_path)
        current_path.pop()

    traverse("you", [])

    # print('\n'.join([', '.join(x) for x in results]))
    print(f"total={len(results):,}")


if __name__ == "__main__":
    # main('example.txt')
    main('input.txt')
