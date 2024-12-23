import networkx as nx  # sorry


def day23(inp):
    connections = inp.splitlines()

    G = nx.Graph([connection.split('-') for connection in connections])
    cliques = list(nx.enumerate_all_cliques(G))
    part1 = sum(
        1
        for clique in cliques
        if len(clique) == 3
        and any(node.startswith('t') for node in clique)
    )
    max_clique = max(cliques, key=len)
    part2 = ','.join(sorted(max_clique))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day23.testinp').read()
    print(day23(testinp))
    inp = open('day23.inp').read()
    print(day23(inp))
