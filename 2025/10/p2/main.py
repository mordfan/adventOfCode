#!/bin/python3
# https://adventofcode.com/2025/day/10#part2

from os import path
from collections.abc import Iterator
from math import pow
from itertools import chain, combinations
from functools import reduce, cache


def get_data(file_name: str) -> Iterator[tuple[str, list[list[int]], list[int]]]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            assert line.startswith('['), "invalid begining of line"

            # light diagram
            b = 0
            e = line.find(']', b)
            assert e > b, "could not locate light diagram"
            ld = line[b + 1:e]

            # button wirings
            b = e + 1
            e = line.find('{', b)
            assert e > b, "could not locate button wiring"
            bw = list([list(list(map(int, x.split(',')))) for x in line[b + 1: e - 2].lstrip('(').rstrip(')').split(') (')])

            # joltage requirements
            b = e + 1
            e = line.find('}', b)
            assert e > b, "could not locate joltage requirements"
            jr: list[int] = list(map(int, line[b:e].split(',')))

            # return
            yield (ld, bw, jr)


def list_to_bin(data: list[int]) -> int:
    return int(sum([(1 * pow(2, i) if i in data else 0) for i in range(0, max(data) + 1)]))


@cache
def get_combos(length: int) -> list[list[int]]:
    s = list(range(length))
    combos = list(chain.from_iterable(combinations(s, r) for r in range(1, length + 1)))
    return combos


def find_best_combo(joltage: list[int], wiring: list[list[int]]) -> int | None:
    print(f"{joltage=})\n{wiring=}")
    counters = {i: x for i, x in enumerate(joltage) if x > 0}
    ret: int | None = None
    length = len(joltage)
    fmt = f"{{:0{length}b}}"
    joltage_bin = list_to_bin([i for (i, n) in enumerate(joltage) if n > 0])
    wiring_bin = [list_to_bin(w) for w in wiring]
    print(f"wiring_bin={[fmt.format(w) for w in wiring_bin]}")
    print(f"joltage_bin={fmt.format(joltage_bin)}")

    for combos_indices in get_combos(len(wiring)):
        # checking if combination covers joltage
        combos_bin = reduce(lambda t, c: t | wiring_bin[c], combos_indices, 0)
        if combos_bin != joltage_bin:
            continue
        combos = [wiring[c] for c in combos_indices]
        print(f"  combos={fmt.format(combos_bin)} ({'good' if combos_bin == joltage_bin else 'bad'}) {combos}")

        # todo: now need to figure out a way to calculate best solution
        cnt = counters.copy()
        total = 0
        x = get_combos(len(combos_indices))

        # for c in x:  # sorted(combos, key=lambda x: len(wiring[x]), reverse=True):
        #     print(f"    c={c}")

        if total > 0 and (ret is None or ret > total):
            ret = total

    return ret


def main(file_name: str) -> None:
    total: int = 0
    for line, (_, wiring, joltage) in enumerate(get_data(file_name)):
        n = find_best_combo(joltage, wiring)
        # assert n is not None, f"no solution for {line=}"
        print('---')
        if n is not None:
            total += n

    print(f"{total=:,}")


if __name__ == "__main__":
    main('example.txt')
    # main('input.txt')
