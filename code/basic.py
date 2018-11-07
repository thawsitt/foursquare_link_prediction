import snap
import matplotlib.pyplot as plt
import cPickle as pickle
from collections import defaultdict, Counter
from pprint import pprint

# TODO: See if a user check into a venue multiple times. Ans: YES

def plot_degree_distribution(graph):
    X, Y = [], []
    N = graph.GetNodes()
    degreeToNumNodes = defaultdict(int)
    for NI in graph.Nodes():
        degree = NI.GetOutDeg()
        degreeToNumNodes[degree] += 1
    for degree in sorted(degreeToNumNodes):
        X.append(degree)
        Y.append(degreeToNumNodes[degree] / float(N))
    plt.loglog(X, Y)
    plt.xlabel('Node Degree (log)')
    plt.ylabel('Proportion of Nodes with a Given Degree (log)')
    plt.title('Degree Distribution of Foursquare Checkins Network')
    plt.show()

def train(graph, users, venues):
    distances = []
    max_wcc = get_nodes_in_max_wcc(graph)
    for u in users:
        print('Finding distances for user: {}'.format(u))
        for v in venues:
            if u in max_wcc and v in max_wcc:
                distance = get_distance(graph, u, v)
                distances.append(((u, v), distance))
                # print('Distance between nodes {}: {}'.format((u,v), distance))
    for item in sorted(distances, key=lambda x: x[1]):
        print(item)

    with open('distances.pickle', 'w') as file:
        pickle.dump(distances, file, protocol=pickle.HIGHEST_PROTOCOL)

def get_distance(graph, u, v):
    S, D = set([u]), set([v])
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

#*******************************************************************************
# Helper functions
#*******************************************************************************

def get_neighbors(NI):
    neighbors = set()
    for i in range(NI.GetDeg()):
        neighbor_node_id = NI.GetNbrNId(i)
        neighbors.add(neighbor_node_id)
    return neighbors

def load_pickles():
    # Load user IDs and venue IDs sets from pickle objects
    with open('user_ids.pickle', 'r') as file:
        users = pickle.load(file)
    with open('venue_ids.pickle', 'r') as file:
        venues = pickle.load(file)
    return users, venues

def load_graph(input_filename):
    graph = snap.LoadEdgeList(snap.PUNGraph, input_filename, 0, 1)
    print('Number of nodes: {}'.format(graph.GetNodes()))
    print('Number of edges: {}'.format(graph.GetEdges()))
    return graph

def print_connected_components(graph):
    components = snap.TCnComV()
    snap.GetWccs(graph, components)
    print('Number of connected components in the graph: {}'.format(len(components)))
    size_to_num_components = Counter([c.Len() for c in components])
    print('Below, you can see a dictionary mapping from')
    print('size (# of nodes in the component) => # of components')
    print('e.g. The largest WCC contains 497806 nodes.')
    pprint(size_to_num_components)

def get_nodes_in_max_wcc(graph):
    # Returns a list of nodes that belong in the largest weakly connected component
    max_wcc = snap.GetMxWcc(graph)
    return set([NI.GetId() for NI in max_wcc.Nodes()])


#*******************************************************************************

def main():
    users, venues = load_pickles()
    graph = load_graph('checkins.txt')
    print_connected_components(graph)
    # plot_degree_distribution(graph)
    train(graph, users, venues)

if __name__ == '__main__':
    main()
