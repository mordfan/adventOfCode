#!/bin/python3
# https://adventofcode.com/2025/day/11#part2

from os import path
from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass(frozen=False)
class Node:
    name: str = field()
    outgoing: list[str] = field(init=False)
    incomming: list[str] = field(init=False)

    def __post_init__(self):
        self.outgoing = []
        self.incomming = []


def get_data(file_name: str) -> Iterator[tuple[str, list[str]]]:
    with open(path.join('..', 'data', file_name), mode='r', encoding='utf-8') as file:
        while (line := file.readline().rstrip()):
            i = line.find(':')
            assert i > 0, "invalid input!"

            name = line[:i]
            outgoing = list(line[i + 2:].split(' '))

            yield (name, outgoing)


def get_connections(file_name: str) -> dict[str, Node]:
    ret: dict[str, Node] = {}
    for (name, outgoing) in get_data(file_name):
        if name not in ret.keys():
            ret[name] = Node(name)
        ret[name].outgoing.extend(outgoing)

        for o in outgoing:
            if o not in ret.keys():
                ret[o] = Node(o)
            ret[o].incomming.append(name)

    # assertions
    assert sum([len(n.incomming) for n in ret.values()]) == sum([len(n.outgoing) for n in ret.values()]), "number of incomming nodes is not equal to number of outgoing nodes"
    keys_set = set(ret.keys())
    for n in ret.values():
        inc_set = set(n.incomming)
        out_set = set(n.outgoing)
        assert len(n.incomming) == len(inc_set), "duplicated incomming nodes"
        assert len(n.outgoing) == len(out_set), "duplicated outgoing nodes"
        assert len(inc_set.intersection(out_set)) == 0, "intersecting nodes"
        assert len(inc_set.intersection(keys_set)) == len(inc_set), "some incomming nodes are not included in keys"
        assert len(out_set.intersection(keys_set)) == len(out_set), "some outgoing nodes are not included in keys"

    return ret


def kahn_topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """
    :param nodes: dictionary of nodes where key is a node and value are nodes that key node depends
    :return: nodes in topological order
    """
    # theory: https://en.wikipedia.org/wiki/Topological_sorting
    # implementation: https://dev.to/leopfeiffer/topological-sort-with-kahns-algorithm-3dl1

    indegrees = {k: 0 for k in graph.keys()}
    for dependencies in graph.values():
        for dep in dependencies:
            indegrees[dep] += 1

    queue: list[str] = [k for k in graph.keys() if indegrees[k] == 0]  # get all starting nodes (these which do not depend on others)
    assert queue, "no starting nodes"

    ret: list[str] = []

    while queue:
        curr = queue.pop(0)
        ret.append(curr)

        for dep in graph[curr]:
            indegrees[dep] -= 1

            if indegrees[dep] == 0:
                queue.append(dep)

    assert len(ret) == len(graph), "circular dependency found"

    return ret


def count_paths(
        graph: dict[str, list[str]],
        start_node: str,
        end_node: str) -> int:
    """Returns number of all possible paths between start_node and end_node using topological sort"""
    # source: https://www.geeksforgeeks.org/dsa/count-possible-paths-two-vertices/
    sorted_graph = kahn_topological_sort(graph)
    assert start_node in sorted_graph, "start_node not in graph"
    assert end_node in sorted_graph, "end_node not in graph"
    ways: dict[str, int] = {n: 0 for n in sorted_graph}
    ways[start_node] = 1

    for node in sorted_graph:
        for dep in graph[node]:
            ways[dep] += ways[node]

    ret = ways[end_node]
    print(f"{start_node=}, {end_node=}, number_of_paths={ret:,}")
    return ret


def main(file_name: str) -> None:
    connections = get_connections(file_name)
    graph = {k: v.outgoing for k, v in connections.items()}

    count_paths(graph, "you", "out")
    count_paths(graph, "svr", "out")
    print("---")
    number_of_paths = count_paths(graph, "svr", "dac")
    number_of_paths *= count_paths(graph, "dac", "fft")  # return 0
    number_of_paths *= count_paths(graph, "fft", "out")
    print(f"{number_of_paths=:,}")
    print("---")
    number_of_paths = count_paths(graph, "svr", "fft")
    number_of_paths *= count_paths(graph, "fft", "dac")
    number_of_paths *= count_paths(graph, "dac", "out")
    print(f"{number_of_paths=:,}")


if __name__ == "__main__":
    # main('example.txt')
    # main('example2.txt')
    main('input.txt')
