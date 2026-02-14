#!/bin/python3
# https://adventofcode.com/2025/day/5#part2

from os import path
from collections.abc import Iterator


def get_ingredients(file_name: str) -> Iterator[int | tuple[int, int]]:
    with open(path.join('..', '..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline()):
            if len(line) <= 1:
                continue
            si = line.find('-')
            if si < 0:
                yield int(line.rstrip())
            else:
                yield (int(line[:si]), int(line[si+1:]))


def main(file_name: str) -> None:
    ranges: list[tuple[int, int]] = []
    for val in get_ingredients(file_name):
        if not (type(val) is tuple and len(val) == 2):
            continue
        ranges.append(val)
    print(f"ranges count={len(ranges)}")
    loops: int = 0
    cr: int = 0
    while cr < len(ranges):
        cmin, cmax = ranges[cr]
        print(f"{cmin=}-{cmax=} @ {cr=} / {len(ranges)}")
        found = True
        while found:  # and cr < len(ranges):
            print("  ***")
            found = False
            ir: int = cr + 1
            while ir < len(ranges):
                (imin, imax) = ranges[ir]
                loops += 1
                if imin >= cmin and imax <= cmax:  # incomming range includes in current range
                    found = True
                    print(f"  >< {imin=}-{imax=}")
                    del ranges[ir]
                    continue
                elif imin < cmin and imax > cmax:  # incomming range extends current range to both sides
                    cmin = imin
                    print(f"  <> {imin=}-{imax=} -> {cmin=}->{imin}, {cmax=}->{imax}")
                    cmax = imax
                    found = True
                    del ranges[ir]
                    continue
                elif imin < cmin and cmin <= imax <= cmax:  # incomming range extends current range to the left
                    print(f"  <  {imin=}-{imax=} -> {cmin=}->{imin}")
                    cmin = imin
                    found = True
                    del ranges[ir]
                    continue
                elif imax > cmax and cmin <= imin <= cmax:  # incomming range extends current range to the right
                    print(f"   > {imin=}-{imax=} -> {cmax=}->{imax}")
                    cmax = imax
                    found = True
                    del ranges[ir]
                    continue
                # else:  # incomming range does not overlap in current one
                #    print(f"  !!  {imin=}-{imax=}")

                ir += 1
        ranges[cr] = (cmin, cmax)
        cr += 1

    print("===")
    i: int = 0
    total: int = 0
    for (cmin, cmax) in sorted(ranges):
        i = (cmax - cmin + 1)
        total += i
        # print(f"{cmin}-{cmax}={i}")
    print(f"{total=:,}")
    print(f"{loops=}")


if __name__ == '__main__':
    # main('test.txt')
    # main('example.txt')
    main('input.txt')
