#!/bin/python3
# https://adventofcode.com/2024/day/2#part2

from os import path
from collections.abc import Iterator


def get_reports(file_name: str) -> Iterator[list[int]]:
    with open(path.join('data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            yield list(map(int, line.split(' ')))


def main(file_name: str) -> None:
    safe_reports: list[int] = []
    for (repId, report) in enumerate(get_reports(file_name)):
        errors: int = 0
        is_safe = False
        trend: bool | None = None
        for i in range(2, len(report)):
            diff = report[i] - report[i - 1]
            if abs(diff) > 3:
                errors += 1
            if trend is not None and trend != (diff > 0):
                errors += 1
            if errors > 1:
                break
            trend = (diff > 0)
        else:
            is_safe = True
            safe_reports.append(repId)

        print(f"{repId=:>3}, {errors=}, safe={('T' if is_safe else 'F')}, {trend=}, {report=}")
        if is_safe:
            safe_reports.append(repId)
    # print(f"{safe_reports=}")
    print(f"number of safe reports = {len(safe_reports)}")


if __name__ == '__main__':
    main('example.txt')
    # main('input.txt')
