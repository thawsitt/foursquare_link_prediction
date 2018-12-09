import snap
import heuristics
import time
import random

def train(graph, users, venues, score_fn, neighbor_dict):
    print('Calculating scores for the training set...')
    start = time.clock()
    scores = []
    num_iterations = 0
    for u in users:
        for v in venues:
            score = score_fn(graph, u, v, neighbor_dict)
            scores.append(((u, v), score))
            num_iterations += 1
            if (num_iterations % 1000 == 0):
                print('Time taken: {0:.2f}s, # iterations: {1}'.format(time.clock() - start, num_iterations))
    print('Calculations complete! Time taken: {0:.2f}s'.format(time.clock() - start))
    print('Top 10 most similar nodes')
    scores.sort(key=lambda x: x[1], reverse=True)
    for item in scores[:10]:
        print(item)
    return scores

def validate(edges, scores):
    TP = 0
    FP = 0
    cutoff = int(len(scores) * 0.2)
    # Take top 20% of the scores
    for node_pair, score in scores[:cutoff]:
        u, v = node_pair
        if (u, v) in edges or (v, u) in edges:
            TP += 1
        else:
            FP += 1
    FN = len(edges) - TP
    print('# TP: {}'.format(TP))
    print('# FP: {}'.format(FP))
    print('# FN: {}'.format(FN))
    print('# edges in test: {}'.format(len(edges)))
    print('Accuracy: {0:.2f}%'.format(TP * 100.0 / len(edges)))
    print('Precision: {0:.2f}%'.format(float(TP) / (TP + FP)))
    print('Recall: {0:.2f}%'.format(float(TP) / (TP + FN)))

def remove_edges(training_graph):
    # Train: 80%, Test: 20%
    num_edges_to_remove = int(training_graph.GetEdges() * 0.2)
    nodes = [node.GetId() for node in training_graph.Nodes()]
    removed_edges = set()
    while num_edges_to_remove > 0:
        node = random.choice(nodes)
        NI = training_graph.GetNI(node)
        if NI.GetDeg() < 2:
            continue
        neighbors = get_neighbors(NI)
        random_neighbor = random.choice(tuple(neighbors))
        training_graph.DelEdge(node, random_neighbor)
        removed_edges.add((node, random_neighbor))
        num_edges_to_remove -= 1
    return removed_edges

def main():
    score_fns = {
        0: heuristics.distance,
        1: heuristics.num_common_neighbors_user,
        2: heuristics.num_common_neighbors_venue,
        3: heuristics.preferential_attachment,
        4: heuristics.katz
    }
    SCORE_FN = score_fns[3]
    training_graph = load_graph('../data/processed/sampled_checkins.txt')
    edges = remove_edges(training_graph)
    users, venues = split_user_venues(training_graph)
    neighbor_dict = create_neighbor_dict(training_graph)
    scores = train(training_graph, users, venues, SCORE_FN, neighbor_dict)
    validate(edges, scores)

#*******************************************************************************
# Helper functions
#*******************************************************************************

def load_graph(input_filename):
    graph = snap.LoadEdgeList(snap.PUNGraph, input_filename, 0, 1)
    print('Number of nodes: {}'.format(graph.GetNodes()))
    print('Number of edges: {}'.format(graph.GetEdges()))
    return graph

def split_user_venues(graph):
    MAX_USER_ID = 2153502
    users = set()
    venues = set()
    for node in graph.Nodes():
        id = node.GetId()
        if id <= MAX_USER_ID:
            users.add(id)
        else:
            venues.add(id)
    return users, venues

def create_neighbor_dict(graph):
    """
    Create a cache of the neighbors of all nodes in the graph
    to speed up score calculations.
    """
    neighbor_dict = {}
    for node in graph.Nodes():
        node_id = node.GetId()
        neighbors = tuple(get_neighbors(node))
        neighbor_dict[node_id] = neighbors
    assert len(neighbor_dict) == graph.GetNodes()
    return neighbor_dict

def get_neighbors(NI):
    neighbors = set()
    for i in range(NI.GetDeg()):
        neighbor_node_id = NI.GetNbrNId(i)
        neighbors.add(neighbor_node_id)
    return neighbors

if __name__ == '__main__':
    main()
