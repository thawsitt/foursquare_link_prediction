import snap
import heuristics
import time

def train(graph, users, venues, score_fn):
    start = time.clock()
    scores = []
    for u in users:
        for v in venues:
            score = score_fn(graph, u, v)
            scores.append(((u, v), score))
    print('Calculations complete! Time taken: {}s'.format(time.clock() - start))
    print('Top 10 most similar nodes')
    for item in sorted(scores, key=lambda x: -x[1])[:10]:
        print(item)

def main():
    graph = load_graph('../data/processed/sampled_checkins.txt')
    users, venues = split_user_venues(graph)
    score_fn = heuristics.num_common_neighbors_venue
    train(graph, users, venues, score_fn)

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
