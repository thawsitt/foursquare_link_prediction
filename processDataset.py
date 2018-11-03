'''
This script processes the original foursquare .dat files downloaded from:
    https://archive.org/details/201309_foursquare_dataset_umn


UserID: UserIDs and VenueIDs overlap. To resolve this, the max UserID is
recorded in the global maxUserID and added to every UserID in each file.

'''
import csv
import string
import os.path
import re

exclude = string.punctuation
path = './umn_foursquare_datasets/'
datFiles = [
        'users.dat',
        'venues.dat',
        'socialgraph.dat',
        'checkins.dat',
        'ratings.dat']

outFiles = [
        'users.tsv',
        'venues.tsv',
        'socialgraph.tsv',
        'checkins.tsv',
        'ratings.tsv']
headers = {
        outFiles[0]: ['userId', 'latitude', 'longitude'],
        outFiles[1]: ['venueId', 'latitude', 'longitude'],
        outFiles[2]: [],
        outFiles[3]: [],
        outFiles[4]: [],
        }

MAX_USER_ID = -1


def outputTsvFile(path, data):
    pass

def processUsers():
    global MAX_USER_ID
    # Get max user id
    with open(path + datFiles[0]) as f:
        line = f.readline()
        count = 0
        while line:
            splitLine = re.sub('\s+[\|]\s+', '\t', line).split()
            if (not splitLine
                    or '--' in splitLine[0] 
                    or splitLine[0].isalpha() 
                    or '(' in splitLine[0]):
                line = f.readline()
                continue

            if int(splitLine[0]) > MAX_USER_ID:
                MAX_USER_ID = int(splitLine[0])
            line = f.readline()


    print 'max user id %d' % (MAX_USER_ID)

    with open(path + datFiles[0]) as f, open(path + outFiles[0], 'w') as tsvFile:
        out = csv.writer(tsvFile, delimiter="\t")
        # Write header
        out.writerow(headers[outFiles[0]])

        line = f.readline()
        count = 0
        while line:
            l = re.sub('\s+[\|]\s+', '\t', line)
            splitLine = l.split()
            if (not splitLine
                    or '--' in splitLine[0] 
                    or splitLine[0].isalpha() 
                    or '(' in splitLine[0]):
                line = f.readline()
                continue

            splitLine[0] = str(int(splitLine[0]) + MAX_USER_ID)
            out.writerow(splitLine)
            line = f.readline()


def processCheckins():
    pass
def processRatings():
    pass
def processSocialGraph():
    pass
def processVenues():
    pass


def main():
    print 'Expecting original datasets at \"%s"\"' % (path)
    warning = """
    WARNING: This will overwrite existing .tsv dataset at ' + path. Continue?
    """
    # TODO
    #  userInput = raw_input(warning)
    userInput = 'y'
    if userInput == 'y' or userInput == 'Y' or userInput == 'yes' or userInput == 'Yes':
        processUsers()
        processCheckins()
        processRatings()
        processSocialGraph()
        processVenues()

if __name__ == '__main__':
        main()
