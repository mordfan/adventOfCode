#!/bin/python3
# https://adventofcode.com/2024/day/2

from os import path
from collections.abc import Iterator


def get_reports(file_name: str) -> Iterator[list[int]]:
    with open(path.join('data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            yield list(map(int, line.split(' ')))


def main(file_name: str) -> None:
    safe_reports: list[int] = []
    for (repId, report) in enumerate(get_reports(file_name)):
        diffs = [report[i] - report[i - 1] for i in range(1, len(report))]
        is_safe = False
        if all(0 < v <= 3 for v in diffs):
            is_safe = True
        elif all(0 > v >= -3 for v in diffs):
            is_safe = True
        print(f"{repId=:>3}, safe={('T' if is_safe else 'F')}, {diffs=}, {report=}")
        if is_safe:
            safe_reports.append(repId)
    # print(f"{safe_reports=}")
    print(f"number of safe reports = {len(safe_reports)}")


if __name__ == '__main__':
    # main('example.txt')
    main('input.txt')
