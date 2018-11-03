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
path = '../umn_foursquare_datasets/'
datFiles = [
        'users.dat',
        'venues.dat',
        'socialgraph.dat',
        'checkins.dat',
        'ratings.dat',
        ]

outFiles = [
        'users.txt',
        'venues.txt',
        'socialgraph.txt',
        'checkins.txt',
        'ratings.txt',
        ]

MAX_USER_ID = -1


def processUsers():
    global MAX_USER_ID
    splitLines = []
    # Get max user id
    with open(path + datFiles[0]) as f:
        lines = f.readlines()
        for line in lines:
            try:
                splitLine = re.sub('\s+[\|]\s+', '\t', line).split()
                if (not splitLine
                        or '--' in splitLine[0] 
                        or splitLine[0].isalpha() 
                        or '(' in splitLine[0]):
                    continue
                if int(splitLine[0]) > MAX_USER_ID:
                    MAX_USER_ID = int(splitLine[0])

                splitLines.append(splitLine)
            except:
                print 'ERROR. splitLine = %s' % (splitLine)


        # Output formatted file
        with open(path + outFiles[0], 'w') as tsvFile:
            out = csv.writer(tsvFile, delimiter="\t")
            for line in lines:
                if line[0] == '--':
                    out.writerow()
                    continue
                # TODO Print line


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
    userInput = raw_input(warning)
    if userInput == 'y' or userInput == 'Y' or userInput == 'yes' or userInput == 'Yes':
        processUsers()
        processCheckins()
        processRatings()
        processSocialGraph()
        processVenues()

if __name__ == '__main__':
        main()
