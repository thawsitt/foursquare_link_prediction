"""
processCheckIns.py
------------------
Author: Thawsitt Naing, Francisco Izaguirre
Date created: 11/04/2018

Input: Foursquare "checkins" dataset
Output: Text file with user_id and venue_id columns e.g. "11234 3435322"

Notes:
- max_user_id is added to venue ids to eliminate overlap between user and venue ids.
- Tested with Python 2.7

Number of unique users: 485381
Number of unique venues: 83999
Max user id: 2153502
Min venue id: 2153503

checkins.dat header
id | user_id | venue_id | latitude | longitude | created_at      
"""

import cPickle as pickle
from geopy.geocoder import Nominatim

geolocator = Nominatim(user_agent="224W_Project")

'''
Checks whether coordinates point to a location in California.
Last three 
Input:  Accepts two strings for long and lat. 
Returns: False if None or empty string.
'''
# TODO Remove first line when ready to use
def located_in_CA(latitude, longitude):
    return True
    if not latitude or not longitude:
        return False
    coords = '%s, %s' % (latitude, longitude)
    location = geolocator.reverse(coords)
    addr = location.split(' ,')
    # last 3 in list are 'state, zip code, USA'
    state = addr[-3]
    country = addr[-1]
    return state == 'California' and country == 'USA'


def read_input(input_filename, max_user_id):
    user_venue_pairs = []
    users, venues = set(), set()
    with open(input_filename, 'r') as input:
        for i, line in enumerate(input):
            parsed = [str.strip() for str in line.split('|')]
            if i <= 1 or len(parsed) < 6:
                print('skipped: {}'.format(parsed))
                continue
            user_id = int(parsed[1])
            venue_id = int(parsed[2]) + max_user_id
            latitude = parsed[3]
            longitude = parsed[4]
            # California checkins only
            if located_in_CA(latitude, longitude):
                users.add(user_id)
                venues.add(venue_id)
                user_venue_pairs.append((user_id, venue_id))

    # Save users and venues objects for future use
    with open('code/user_ids.pickle', 'w') as file:
        pickle.dump(users, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open('code/venue_ids.pickle', 'w') as file:
        pickle.dump(venues, file, protocol=pickle.HIGHEST_PROTOCOL)

    print_metrics(users, venues)
    assert(len(users.intersection(venues)) == 0)
    return user_venue_pairs


def write_output_files(user_venue_pairs, split_train_test, percent_train, output_filenames):
    all, train, test = output_filenames
    if split_train_test:
        total_pairs = len(user_venue_pairs)
        cutoff_index = int(total_pairs * percent_train)
        with open(train, 'w') as training_set, open(test, 'w') as test_set:
            for i, pair in enumerate(user_venue_pairs):
                user_id, venue_id = pair
                if i < cutoff_index:
                    training_set.write('{}\t{}\n'.format(user_id, venue_id))
                else:
                    test_set.write('{}\t{}\n'.format(user_id, venue_id))
    else:
        with open(all, 'w') as checkins:
            for i, pair in enumerate(user_venue_pairs):
                user_id, venue_id = pair
                checkins.write('{}\t{}\n'.format(user_id, venue_id))


def print_metrics(users, venues):
    print('Number of unique users: {}'.format(len(users)))
    print('Number of unique venues: {}'.format(len(venues)))
    print('User id range: {} to {}'.format(min(users), max(users)))
    print('Venue id range: {} to {}'.format(min(venues), max(venues)))


def main():
    input_filename = 'umn_foursquare_datasets/checkins.dat'
    output_all = 'code/checkins.txt'
    output_train = 'code/train.txt'
    output_test = 'code/test.txt'
    max_user_id = 2153502   # pre-computed
    split_train_test = False # Set to False to get only one output file

    user_venue_pairs = read_input(input_filename, max_user_id)
    write_output_files(user_venue_pairs, split_train_test, 0.5, (output_all, output_train, output_test))


if __name__ == '__main__':
    main()
