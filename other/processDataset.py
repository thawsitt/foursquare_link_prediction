'''
This script processes the original foursquare .dat files downloaded from:
    https://archive.org/details/201309_foursquare_dataset_umn,
and outputs .tsv files to directory umn_foursquare_datasets

Instructions:
1) Download the dataset folder from the link above
2) Run script: python processDataset.py
    ~5 minutes
3) Import .tsv files into snap

Note:
UserID: UserIDs and VenueIDs overlap. To resolve this, the max UserID is
recorded in the global maxUserID and added to every UserID in each file.
'''

import csv
import string
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
        outFiles[2]: ['userId', 'userId'],
        outFiles[3]: ['id', 'userId', 'venueId', 'latitude', 'longitude', 'createdAt'],
        outFiles[4]: ['userId', 'venueId', 'rating'],
        }

MAX_USER_ID = -1

def processUsers():
    print 'Processing Users...'
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


def processVenues():
    print 'Processing Venues...'
    with open(path + datFiles[1]) as f, open(path + outFiles[1], 'w') as tsvFile:
        out = csv.writer(tsvFile, delimiter="\t")
        # Write header
        out.writerow(headers[outFiles[1]])

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

            out.writerow(splitLine)
            line = f.readline()


def processSocialGraph():
    print 'Processing Social Graph...'
    with open(path + datFiles[2]) as f, open(path + outFiles[2], 'w') as tsvFile:
        out = csv.writer(tsvFile, delimiter="\t")
        # Write header
        out.writerow(headers[outFiles[2]])

        line = f.readline()
        count = 0
        while line:
            l = re.sub('\s+[\|]\s+', '\t', line)
            splitLine = l.split()
            if (not splitLine
                    or '--' in splitLine[0] 
                    or '_' in splitLine[0]
                    or splitLine[0].isalpha()   
                    or '(' in splitLine[0]):
                line = f.readline()
                continue

            splitLine[0] = str(int(splitLine[0]) + MAX_USER_ID)
            splitLine[1] = str(int(splitLine[1]) + MAX_USER_ID)
            out.writerow(splitLine)
            line = f.readline()


def processCheckins():
    print 'Processing Checkins...'
    with open(path + datFiles[3]) as f, open(path + outFiles[3], 'w') as tsvFile:
        out = csv.writer(tsvFile, delimiter="\t")
        # Write header
        out.writerow(headers[outFiles[3]])

        line = f.readline()
        count = 0
        while line:
            # Replace empty Lat/Long with NULL
            l = re.sub('[\|][\s]+[\|][\s]+[\|]', '| NULL | NULL |', line)  
            l = re.sub('\s+[\|]\s+', '\t', l)

            splitLine = l.split()
            if (not splitLine
                    or '--' in splitLine[0] 
                    or splitLine[0].isalpha() 
                    or '(' in splitLine[0]):
                line = f.readline()
                continue

            splitLine[1] = str(int(splitLine[1]) + MAX_USER_ID)
            # Concate date
            splitLine[5] = splitLine[5] + '_' + splitLine[6]
            splitLine = splitLine[:6]

            assert len(splitLine) == 6
            out.writerow(splitLine)
            line = f.readline()


def processRatings():
    print 'Processing Ratings...'
    with open(path + datFiles[4]) as f, open(path + outFiles[4], 'w') as tsvFile:
        out = csv.writer(tsvFile, delimiter="\t")
        # Write header
        out.writerow(headers[outFiles[4]])

        line = f.readline()
        count = 0
        while line:
            l = re.sub('\s+[\|]\s+', '\t', line)
            splitLine = l.split()
            if (not splitLine
                    or '--' in splitLine[0] 
                    or '_' in splitLine[0]
                    or splitLine[0].isalpha() 
                    or '(' in splitLine[0]):
                line = f.readline()
                continue

            splitLine[0] = str(int(splitLine[0]) + MAX_USER_ID)
            out.writerow(splitLine)
            line = f.readline()


def main():
    print 'Expecting original datasets at \"%s"\"' % (path)
    warning = """
    WARNING: This will overwrite existing .tsv dataset at ' + path. Continue?
    """
    userInput = raw_input(warning)
    if userInput == 'y' or userInput == 'Y' or userInput == 'yes' or userInput == 'Yes':
        processUsers()
        processVenues()
        processSocialGraph()
        processCheckins()
        processRatings()

if __name__ == '__main__':
        main()
