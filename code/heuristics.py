"""
heuristics.py
-------------
Contains various similarity metrics used in link prediction.
"""

import snap
import random
from collections import Counter
from math import log

def random_predictor(graph, x, y, neighbor_dict):
    """
    Random predictor
    """
    return random.choice([0, 1])

def distance(graph, x, y, neighbor_dict):
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
            for neighbor in neighbor_dict[node]:
                new_nodes.add(neighbor)
        smaller_set.update(new_nodes)
        num_steps += 1
    return num_steps * -1


def num_common_neighbors_user(graph, user, venue, neighbor_dict):
    """
    The number of common neighbors. For bipartite network, we adapt this as:
    max(N(user) intersect N(user_i)) for all user_i in N(venue)
    where N(x) means neighbors of x.
    """
    s1 = set(neighbor_dict[user])
    max_score = 0
    for user_i in neighbor_dict[venue]:
        s2 = set(neighbor_dict[user_i])
        score = len(s1.intersection(s2))
        max_score = max(score, max_score)
    return max_score

def num_common_neighbors_venue(graph, user, venue, neighbor_dict):
    """
    The number of common neighbors. For bipartite network, we adapt this as:
    max(N(venue) intersect N(venue_i)) for all venue_i in N(user)
    where N(x) means neighbors of x.
    """
    s1 = set(neighbor_dict[venue])
    max_score = 0
    for venue_i in neighbor_dict[user]:
        s2 = set(neighbor_dict[venue_i])
        score = len(s1.intersection(s2))
        max_score = max(score, max_score)
    return max_score


def adamic_adar_user(graph, user, venue, neighbor_dict):
    """
    Weighted common neighbors
    """
    s1 = set(neighbor_dict[user])
    max_intersect = set()
    for user_i in neighbor_dict[venue]:
        s2 = set(neighbor_dict[user_i])
        intersect = s1.intersection(s2)
        if len(intersect) > len(max_intersect):
            max_intersect = intersect
    weighted_score = 0
    for z in max_intersect:
        degree = graph.GetNI(z).GetDeg()
        if degree > 1:
            weighted_score += 1.0 / log(degree)
    return weighted_score


def adamic_adar_venue(graph, user, venue, neighbor_dict):
    """
    Weighted common neighbors
    """
    s1 = set(neighbor_dict[venue])
    max_intersect = set()
    for venue_i in neighbor_dict[user]:
        s2 = set(neighbor_dict[venue_i])
        intersect = s1.intersection(s2)
        if len(intersect) > len(max_intersect):
            max_intersect = intersect
    weighted_score = 0
    for z in max_intersect:
        degree = graph.GetNI(z).GetDeg()
        if degree > 1:
            weighted_score += 1.0 / log(degree)
    return weighted_score


def preferential_attachment(graph, x, y, neighbor_dict):
    """
    Degree(x) * Degree(y)
    """
    degree_x = graph.GetNI(x).GetDeg()
    degree_y = graph.GetNI(y).GetDeg()
    return degree_x * degree_y


def katz(graph, x, y, neighbor_dict):
    """
    Katz (Exponentially Damped Path Counts)
    """
    neighbor_cache = {}
    beta = 0.005
    path_lengths = {}
    path_length = 1
    nodes_to_explore = [x]
    while path_length < 4:
        new_nodes_to_explore = []
        for node in nodes_to_explore:
            neighbors = neighbor_dict[node]
            new_nodes_to_explore.extend(list(neighbors))
        path_lengths[path_length] = Counter(new_nodes_to_explore)[y]
        nodes_to_explore = new_nodes_to_explore
        path_length += 1
    score = 0
    for l in path_lengths:
        score += beta**l * path_lengths[l]
    return score
