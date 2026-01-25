#!/bin/python3
# https://adventofcode.com/2025/day/10#part2
# amazing idea of bifurcatin from r/tenthmascot since all of mine ideas failed...

from os import path
from collections import Counter
from collections.abc import Iterator
from functools import cache
from itertools import chain, combinations
from dataclasses import dataclass, field


def get_key_repr(coverage: list[bool]) -> str:
    return ''.join(['1' if c else '0' for c in coverage])


@dataclass(frozen=True, eq=False, order=False)
class Combo:
    key: tuple[bool, ...] = field(repr=False)
    key_repr: str = field(init=False)
    buttons: list[tuple[int, ...]] = field()
    counters: Counter = field()

    def __post_init__(self) -> None:
        object.__setattr__(self, "key_repr", get_key_repr(self.key))

    def __lt__(self, other) -> bool:
        return self.key == other.key and len(self.buttons) < len(other.buttons)


def get_data(file_name: str) -> Iterator[tuple[list[tuple[int, ...]], tuple[int, ...]]]:
    """:return: tuple[list[wiring: tuple[int, ...]], joltage: tuple[int, ...]]"""
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            _, *wiring, joltage = line.split()
            yield ([tuple(map(int, w[1:-1].split(','))) for w in wiring], tuple(map(int, joltage[1:-1].split(','))))


def get_button_combos(wiring: list[tuple[int, ...]], joltage: tuple[int, ...]) -> dict[str, Combo]:
    """Returns dictionary where:
        :key: is a string representing joltage coverage,
        :value: is Combo dataclass"""
    ret: dict[str, Combo] = {}

    for wiring_indices in chain.from_iterable(combinations(range(len(wiring)), r) for r in range(1, len(wiring) + 1)):
        buttons = tuple([wiring[i] for i in wiring_indices])
        counters = Counter(chain.from_iterable(buttons))
        if any([x > 1 for x in counters.values()]):
            continue  # that eliminates cases where one wire occurs multiple times
        coverage = tuple([counters.get(x, 0) % 2 != 0 for x in range(len(joltage))])
        combo = Combo(coverage, buttons, counters)
        if combo.key not in ret.keys():
            ret[combo.key] = combo
            print(f"  [+] {combo}")
        elif ret[combo.key] > combo:
            print(f"  [v] {ret[combo.key]}")
            ret[combo.key] = combo
            print(f"  [^] {combo}")

    return ret


def find_best_combo(wiring: list[tuple[int, ...]], joltage: tuple[int, ...]) -> int | None:
    print(f"{joltage=}, {wiring=}")
    combos = get_button_combos(wiring, joltage)
    presses: dict[tuple[int, ...], int] = {w: 0 for w in wiring}  # key=button/wiring, value=number of presses
    counters: list[int] = list(joltage)  # copy of joltage

    covered = True
    for n in sorted(set(joltage), reverse=True):
        coverage = get_key_repr([joltage[i] >= n for i in range(len(joltage))])
        # print(f"{n=}, {coverage=}")
        if coverage not in combos.keys():
            print(f"  ..no elligible {coverage=} for {n=}")
            covered = False

    if not covered:
        # for c in sorted(combos):
        #     print(f"  {c=}, {combos[c]=}")
        return 0
    else:
        return 1


def main(file_name: str) -> None:
    total = 0
    for line, (wiring, joltage) in enumerate(get_data(file_name)):
        n = find_best_combo(wiring, joltage)
        # assert n is not None, "no good combo found"
        # assert n > 0, "does that suppose to happen?"
        # total += n
        break
    print(f"{total=:,}")


if __name__ == "__main__":
    main('example.txt')
    # main('input.txt')
