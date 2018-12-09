"""
heuristics.py
-------------
Contains various similarity metrics used in link prediction.
"""

import snap
from math import log


def distance(graph, x, y):
    """
    Negative of the shortest path distance from x to y.

    We exploit the small-world property of the social network and apply
    expanded ring search to compute the shortest path distance from
    x to y efficiently.
    """
    S, D = set([x]), set([y])
    num_steps = 0
    while len(S.intersection(D)) == 0:
        smaller_set = S if len(S) < len(D) else D
        new_nodes = set()
        for node in smaller_set:
            for neighbor in get_neighbors(graph.GetNI(node)):
                new_nodes.add(neighbor)
        smaller_set.update(new_nodes)
        num_steps += 1
    return num_steps * -1


def num_common_neighbors(graph, x, y):
    """
    The number of common neighbors between x and y.
    """
    n1 = get_neighbors(graph.GetNI(x))
    n2 = get_neighbors(graph.GetNI(y))
    assert len(n1.intersection(n2)) == 0
    return 0


def jaccard_coefficient(graph, x, y):
    """
    Number of common neighbors divided by number of total neighbors
    """
    n1 = get_neighbors(graph.GetNI(x))
    n2 = get_neighbors(graph.GetNI(y))
    num_common = len(n1.intersection(n2))
    num_total = len(n1.union(n2))
    return float(num_common) / num_total


def adamic_adar(graph, x, y):
    """
    Weighted common neighbors
    """
    n1 = get_neighbors(graph.GetNI(x))
    n2 = get_neighbors(graph.GetNI(y))
    common_neighbors = n1.intersection(n2)
    weighted_score = 0
    for z in common_neighbors:
        degree = graph.GetNI(z).GetDeg()
        weighted_score += 1.0 / log(degree)
    return weighted_score


def preferential_attachment(graph, x, y):
    """
    Degree(x) * Degree(y)
    """
    degree_x = graph.GetNI(x).GetDeg()
    degree_y = graph.GetNI(y).GetDeg()
    return degree_x * degree_y

#*******************************************************************************
# Helper functions
#*******************************************************************************

def get_neighbors(NI):
    neighbors = set()
    for i in range(NI.GetDeg()):
        neighbor_node_id = NI.GetNbrNId(i)
        neighbors.add(neighbor_node_id)
    return neighbors
