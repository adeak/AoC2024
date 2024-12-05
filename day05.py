from collections import defaultdict
from graphlib import TopologicalSorter


def day05(inp):
    ordering, updates = inp.strip().split('\n\n')

    graph = defaultdict(set)  # page -> {earlier pages}
    for rule in ordering.splitlines():
        earlier, later = map(int, rule.split('|'))
        graph[later].add(earlier)

    ordereds = []
    unordereds = []
    for update in updates.splitlines():
        pages = list(map(int, update.split(',')))
        for i, ref_page in enumerate(pages):
            if any(other_page in graph[ref_page] for other_page in pages[i + 1:]):
                # wrong order (part 2)
                unordereds.append(pages)
                break
        else:
            # correct order (part 1)
            ordereds.append(pages)
            continue

    # part 1
    part1 = sum(pages[len(pages) // 2] for pages in ordereds)

    # part 2
    part2 = 0
    for pages in unordereds:
        subgraph = {key: graph[key] for key in pages}
        sorter = TopologicalSorter(subgraph)
        pages = [page for page in sorter.static_order() if page in set(pages)]
        part2 += pages[len(pages) // 2]

    return part1, part2


if __name__ == "__main__":
    testinp = open('day05.testinp').read()
    print(day05(testinp))
    inp = open('day05.inp').read()
    print(day05(inp))
