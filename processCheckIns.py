"""
processCheckIns.py
------------------
Author: Thawsitt Naing, Francisco Izaguirre
Date created: 11/04/2018

Input: Foursquare "checkins" dataset
Output: Text file with user_id and venue_id columns e.g. "11234 3435322"

Notes:
- MAX_USER_ID is added to venue ids to eliminate overlap between user and venue ids.
- Tested with Python 2.7

Number of unique users: 485381
Number of unique venues: 83999
Max user id: 2153502
Min venue id: 2153503

checkins.dat header
id | user_id | venue_id | latitude | longitude | created_at      

Fraction of nodes in Max WCC = TODO

DATASET REDUCTION
Goal: Reduce dataset to largest weakly connected component where each node has
at least some degree X. Below are some metrics calculated:

    Degree > 1 : 203590 nodes, 548331 edges : 177521 users, 26069 venues
    Degree > 2 :  91654 nodes, 334981 edges :  79670 users, 11984 venues
    Degree > 3 :  42779 nodes, 193949 edges :  36650 users,  6129 venues
    Degree > 4 :  19576 nodes, 104805 edges :  16477 users,  3099 venues
    Degree > 5 :   8094 nodes,  49892 edges :   6678 users,  1416 venues
    Degree > 6 :   3156 nodes,  21574 edges :   2537 users,   619 venues
    Degree > 7 :    613 nodes,   4909 edges :    525 users,    88 venues
    Degree > 8 :    259 nodes,   2154 edges :    205 users,    54 venues

"""

from enum import Enum
import cPickle as pickle
import os
import snap

'''
Checks whether coordinates point to a location in California.
Last three 
Input:  Accepts two strings for long and lat. 
Returns: False if None or empty string.
'''

MAX_USER_ID = 2153502   # pre-computed
SPLIT_TRAIN_TEST = False # Set to False to get only one output file

class Filetype(Enum):
    DAT = 0,
    PICKLE = 1,
    TXT = 2 


class Datafile(Enum):
    CHECKINS_DAT = 0,
    CHECKINS_TXT = 1,
    SAMPLE_CKNS_TXT = 2,
    TEST_TXT = 3, 
    TRAIN_TXT = 4,
    USERS_PICKLE = 5,
    VENUES_PICKLE = 6


Datafiles = {
        Datafile.CHECKINS_TXT    : '../../data/processed/checkins.txt',
        Datafile.CHECKINS_DAT    : '../../data/umn_foursquare_datasets/checkins.dat',
        Datafile.SAMPLE_CKNS_TXT : '../../data/processed/sampled_checkins.txt',
        Datafile.TEST_TXT        : '../../data/test/test.txt',
        Datafile.TRAIN_TXT       : '../../data/training/train.txt',
        Datafile.USERS_PICKLE    : '../../data/pickles/user_ids.pickle',
        Datafile.VENUES_PICKLE   : '../../data/pickles/venue_ids.pickle',
        }


# Makes directory for filename if it doesn't exist
def checkMakeDirectory(filename):
    directory = filename[:filename.rfind('/')]
    try:
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise

def writeFile(filename, data, filetype, header=None):
    if data is None:
        print 'writeFile: data is None. File not written'
        return

    checkMakeDirectory(filename)
    if filetype == Filetype.TXT:
        with open(filename, 'w') as file:
            if header:
                file.write('{}\n'.format(header))
            for item in data:
                for i, elem in enumerate(item):
                    if i == len(item) - 1:
                        file.write('{}\n'.format(elem))
                    else:
                        file.write('{} '.format(elem))
            
    elif filetype == Filetype.PICKLE:
        with open(filename, 'w') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        print 'Filetype not recognized! No file written'


def print_metrics(users, venues):
    print('Number of unique users: {}'.format(len(users)))
    print('Number of unique venues: {}'.format(len(venues)))
    print('User id range: {} to {}'.format(min(users), max(users)))
    print('Venue id range: {} to {}'.format(min(venues), max(venues)))


def read_input(input_filename, MAX_USER_ID):
    user_venue_edges = []
    users, venues = set(), set()
    with open(input_filename, 'r') as input:
        for i, line in enumerate(input):
            parsed = [str.strip() for str in line.split('|')]
            if i <= 1 or len(parsed) < 6:
                #  print('skipped: {}'.format(parsed))
                continue
            user_id = int(parsed[1])
            venue_id = int(parsed[2]) + MAX_USER_ID
            users.add(user_id)
            venues.add(venue_id)
            user_venue_edges.append((user_id, venue_id))

    writeFile(Datafiles[Datafile.USERS_PICKLE], users, Filetype.PICKLE)
    writeFile(Datafiles[Datafile.VENUES_PICKLE], venues, Filetype.PICKLE)

    #  print_metrics(users, venues)
    assert(len(users.intersection(venues)) == 0)
    return user_venue_edges


def splitTrainTest(edges, persent_train):
    total_pairs = len(edges)
    cutoff_index = int(total_pairs * percent_train)
    testEdges, trainEdges = [], []
    for i, edge in enumerate(edges):
        user_id, venue_id = edge
        if i < cutoff_index:
            trainEdges.append((user_id, venue_id))
        else:
            testEdges.append((user_id, venue_id))

    return trainEdges, testEdges


# Filters out nodes that don't have at least degree minDeg
# Returns: list of edges (src node, dst node)
def sampleDatasetBFS(edgeList, minDeg):
    Graph = snap.LoadConnList(snap.PNGraph, edgeList)
    G = snap.GetMxWcc(Graph)
    while True:
        nodesToDel = snap.TIntV()
        for n in G.Nodes():
            if n.GetDeg() < minDeg:
                nodesToDel.Add(n.GetId())
        if nodesToDel.Len() == 0:
            break
        snap.DelNodes(G, nodesToDel)
    nodes, edges = G.GetNodes(), G.GetEdges()

    numUsers, numVenues = 0, 0
    for n in G.Nodes():
        if n.GetInDeg() == 0:
            numUsers += 1
        else:
            numVenues += 1

    print '# of nodes: {}, # of edges: {}'.format(G.GetNodes(), G.GetEdges())
    print '# of users: {}, # of venues: {}'.format(numUsers, numVenues)
    print 'isConnected = {}'.format(snap.IsConnected(G))
    edges = [(e.GetSrcNId(), e.GetDstNId()) for e in G.Edges()]
    return edges


# Returned a set of venues that user has checked in to.
# Input: user is a Node I object
def getAdjacentVenues(G, user):
    venues = set()
    for venueId in user.GetOutEdges():
        venues.add(venueId)
    return venues


# Returned a set of users that have all checked in to Venue
# Input: venue is a Node I object
def getAdjacentUsers(G, venue):
    users = set()
    for userId in venue.GetInEdges():
        users.add(userId)
    return users


def main():
    # Read checkins and write output files
    print 'Reading checkins form {}'.format(Datafiles[Datafile.CHECKINS_DAT])
    edges = read_input(Datafiles[Datafile.CHECKINS_DAT], MAX_USER_ID)
    if SPLIT_TRAIN_TEST:
        print 'Splitting into train/test sets...'
        trainData, testData = splitTrainTest(edges, 0.5)
        print 'Writing train file {}'.format(Datafiles[Datafile.TRAIN_TXT])
        writeFile(Datafiles[Datafile.TRAIN_TXT], trainData, Filetype.TXT)
        print 'Writing test file {}'.format(Datafiles[Datafile.TEST_TXT])
        writeFile(Datafiles[Datafile.TEST_TXT], testData, Filetype.TXT)

    print 'Writing all checkins to {}'.format(Datafiles[Datafile.CHECKINS_TXT])
    writeFile(Datafiles[Datafile.CHECKINS_TXT], edges, Filetype.TXT)

    minDegree = 9
    sampleEdges = sampleDatasetBFS(Datafiles[Datafile.CHECKINS_TXT], minDegree)
    print 'Writing sampled checkins to {}'.format(
            Datafiles[Datafile.SAMPLE_CKNS_TXT])
    writeFile(Datafiles[Datafile.SAMPLE_CKNS_TXT], sampleEdges, Filetype.TXT)
    print 'Sampling complete!'

if __name__ == '__main__':
    main()

