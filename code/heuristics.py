"""
heuristics.py
-------------
Contains various similarity metrics used in link prediction.
"""

import snap
from collections import Counter
from math import log


def distance(graph, x, y):
    """
    Negative of the shortest path distance from x to y.

    We exploit the small-world property of the social network and apply
    expanded ring search to compute the shortest path distance from
    x to y efficiently.
    """
    assert(snap.IsConnected(graph))
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


def num_common_neighbors_user(graph, user, venue):
    """
    The number of common neighbors. For bipartite network, we adapt this as:
    max(N(user) intersect N(user_i)) for all user_i in N(venue)
    where N(x) means neighbors of x.
    """
    n1 = get_neighbors(graph.GetNI(user))
    max_score = 0
    for user_i in get_neighbors(graph.GetNI(venue)):
        n2 = get_neighbors(graph.GetNI(user_i))
        score = len(n1.intersection(n2))
        max_score = max(score, max_score)
    return max_score

def num_common_neighbors_venue(graph, user, venue):
    """
    The number of common neighbors. For bipartite network, we adapt this as:
    max(N(venue) intersect N(venue_i)) for all venue_i in N(user)
    where N(x) means neighbors of x.
    """
    n1 = get_neighbors(graph.GetNI(venue))
    max_score = 0
    for venue_i in get_neighbors(graph.GetNI(user)):
        n2 = get_neighbors(graph.GetNI(venue_i))
        score = len(n1.intersection(n2))
        max_score = max(score, max_score)
    return max_score


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


def katz(graph, x, y):
    """
    Katz (Exponentially Damped Path Counts)
    """
    neighbor_cache = {}
    beta = 0.5
    path_lengths = {}
    path_length = 1
    nodes_to_explore = [x]
    while path_length < 4:
        new_nodes_to_explore = []
        for node in nodes_to_explore:
            if node in neighbor_cache:
                neighbors = neighbor_cache[node]
            else:
                neighbors = get_neighbors(graph.GetNI(node))
                neighbor_cache[node] = neighbors
            new_nodes_to_explore.extend(list(neighbors))
        path_lengths[path_length] = Counter(new_nodes_to_explore)[y]
        nodes_to_explore = new_nodes_to_explore
        path_length += 1
    score = 0
    for l in path_lengths:
        score += beta**l * path_lengths[l]
    return score



#*******************************************************************************
# Helper functions
#*******************************************************************************

def get_neighbors(NI):
    neighbors = set()
    for i in range(NI.GetDeg()):
        neighbor_node_id = NI.GetNbrNId(i)
        neighbors.add(neighbor_node_id)
    return neighbors
