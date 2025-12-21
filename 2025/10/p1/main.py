#!/bin/python3
# https://adventofcode.com/2025/day/10

from os import path
from collections.abc import Iterator
from math import pow
from itertools import chain, combinations


COMBO_CACHE: dict[list[list[int]]] = {}


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


def get_combos(length: int) -> list[list[int]]:
    if length in COMBO_CACHE.keys():
        return COMBO_CACHE[length]
    s = list(range(length))
    combos = list(chain.from_iterable(combinations(s, r) for r in range(1, length + 1)))
    COMBO_CACHE[length] = combos
    return combos


def find_best_combo(lights: str, wiring: list[list[int]]) -> int | None:
    print(f"{lights=}), {wiring=}")

    ret: int | None = None
    length = len(lights)
    fmt = f"{{:0{length}b}}"
    target_bin = list_to_bin([i for i, c in enumerate(lights) if c == '#'])
    wiring_bin: list[int] = [list_to_bin(w) for w in wiring]
    if target_bin in wiring:
        print("   bullseye!")
        return 1

    print(f"target='{fmt.format(target_bin)}'")
    for combos in get_combos(len(wiring)):
        state_bin = 0
        press_cnt = 0
        # print(f"  {combos=}, {' > '.join([fmt.format(wiring_bin[c]) for c in combos])}")
        for c in combos:
            press_cnt += 1
            state_bin ^= wiring_bin[c]

        success = state_bin == target_bin

        if success:
            print(f"    {('success' if success else 'fail')}, (state={fmt.format(state_bin)}), cnt={press_cnt}, {', '.join([str(wiring[c]) for c in combos])}")

        if success and (ret is None or ret > press_cnt):
            ret = press_cnt

    print(f"    best={ret}")
    return ret


def main(file_name: str) -> None:
    total: int = 0
    for line, (lights, wiring, _) in enumerate(get_data(file_name)):
        n = find_best_combo(lights, wiring)
        assert n is not None, f"no solution for {line=}"
        if n is not None:
            total += n

    print(f"\n{total=:,}")


if __name__ == "__main__":
    # main('example.txt')
    main('input.txt')
