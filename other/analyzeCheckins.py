"""
analyzeCheckins.py
------------------
Author: Thawsitt Naing
Date created: 11/06/2018

Analyze Foursquare Checkins dataset.

Note: Use Python 2.7
"""
# Number of unique users: 485381
# Number of unique venues: 83999
# Max user id: 2153502
# Min venue id: 2153503

from collections import defaultdict
import matplotlib.pyplot as plt
from pprint import pprint


# e.g. 23 -> [1, 3, 55, 3]
# User 23 checked into venue 1, 3, 55 and 3.
# Venues is a list, NOT a set. So, there might be duplicates.
def map_user_to_venues(input_filename, max_user_id):
    user_to_venues = defaultdict(list)
    with open(input_filename, 'r') as input:
        for i, line in enumerate(input):
            if i > 1:
                parsed = [str.strip() for str in line.split('|')]
                if len(parsed) < 6:
                    print('skipped: {}'.format(parsed))
                    continue
                user_id = int(parsed[1])
                venue_id = int(parsed[2]) + max_user_id
                user_to_venues[user_id].append(venue_id)
    return user_to_venues


def plot_degree_distribution(user_to_venues):
    degree_to_num_nodes = defaultdict(int)
    for user, venues in user_to_venues.items():
        num_venues = len(venues)
        degree_to_num_nodes[num_venues] += 1
    pprint(degree_to_num_nodes)
    X, Y = [], []
    total_nodes = len(user_to_venues)
    for degree in sorted(degree_to_num_nodes):
        X.append(degree)
        num_nodes = degree_to_num_nodes[degree]
        Y.append(float(num_nodes) / total_nodes)
    plt.loglog(X, Y)
    plt.xlabel('Degree: number of venues checked in (log)')
    plt.ylabel('Proportion of Users with a Given Degree (log)')
    plt.title('Degree Distribution of USER NODES in Foursquare Checkins Network')
    plt.text(8.5, 0.3, '60% of users checked into only 1 venue', fontsize=12)
    plt.grid(axis='y', alpha=0.7)
    plt.show()


def main():
    max_user_id = 2153502
    input_filename = 'umn_foursquare_datasets/checkins.dat'
    user_to_venues = map_user_to_venues(input_filename, max_user_id)
    plot_degree_distribution(user_to_venues)


if __name__ == '__main__':
    main()
