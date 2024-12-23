from collections import defaultdict

import networkx as nx  # sorry


def day23(inp):
    data = inp.splitlines()
    connections = defaultdict(set)
    for connection in data:
        this, that = connection.split('-')
        connections[this].add(that)
        connections[that].add(this)

    seeds = {node for node in connections if node.startswith('t')}
    cliques = set()
    for seed in seeds:
        neighbs = connections[seed]
        for neighb in neighbs:
            next_neighbs = connections[neighb] & neighbs
            for next_neighb in next_neighbs:
                cliques.add(frozenset([seed, neighb, next_neighb]))
    part1 = len(cliques)

    G = nx.Graph()
    for start, ends in connections.items():
        G.add_edges_from([(start, end) for end in ends])
    max_clique = max(nx.find_cliques(G), key=len)
    part2 = ','.join(sorted(max_clique))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day23.testinp').read()
    print(day23(testinp))
    inp = open('day23.inp').read()
    print(day23(inp))
