import snap
import matplotlib.pyplot as plt
from collections import defaultdict

# TODO: See if a user check into a venue multiple times.

def load_graph(input_filename):
    graph = snap.LoadEdgeList(snap.PUNGraph, input_filename, 0, 1)
    print('Number of nodes: {}'.format(graph.GetNodes()))
    print('Number of edges: {}'.format(graph.GetEdges()))
    return graph

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

def main():
    graph = load_graph('checkins.txt')
    plot_degree_distribution(graph)

if __name__ == '__main__':
    main()
