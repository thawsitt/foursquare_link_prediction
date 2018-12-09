import snap
import heuristics
import time

def train(graph, users, venues, score_fn):
    print('Calculating scores for the training set...')
    start = time.clock()
    scores = []
    for u in users:
        for v in venues:
            # if graph.IsEdge(u, v):
            #     continue
            score = score_fn(graph, u, v)
            scores.append(((u, v), score))
    print('Calculations complete! Time taken: {}s'.format(time.clock() - start))
    print('Top 10 most similar nodes')
    scores.sort(key=lambda x: -x[1])
    for item in scores[:10]:
        print(item)
    return scores

def validate(test_graph, scores):
    TP = 0
    FP = 0
    cutoff = len(scores)
    for node_pair, score in scores[:cutoff]:
        u, v = node_pair
        if test_graph.IsEdge(u, v):
            TP += 1
        else:
            FP += 1
    print('# TP: {}'.format(TP))
    print('# FP: {}'.format(FP))
    print('Accuracy: {}%'.format(TP * 100.0 / test_graph.GetEdges()))

def main():
    SCORE_FN = heuristics.num_common_neighbors_venue
    training_graph = load_graph('../data/training/train.txt')
    test_graph = load_graph('../data/test/test.txt')
    users, venues = split_user_venues(training_graph)
    scores = train(training_graph, users, venues, SCORE_FN)
    validate(test_graph, scores)

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

if __name__ == '__main__':
    main()
