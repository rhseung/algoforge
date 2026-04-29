import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import core.graph as g

if __name__ == "__main__":
    u, v, w = g.vertices("u", "v", "w")

    walk_unweighted = u - v - w
    walk_weighted = u - 3 - v - 2 - w

    g1 = g.Graph(walk_unweighted)
    g2 = g.Graph(walk_weighted)
    g3 = g.UnweightedGraph(walk_unweighted)
    g4 = g.WeightedGraph(walk_weighted)
    print(g1, g2, g3, g4, sep="\n")

    g1.show()

    print(walk_unweighted.length, walk_unweighted.vertices)
    print(walk_weighted.length, walk_weighted.weight, walk_weighted.vertices)
