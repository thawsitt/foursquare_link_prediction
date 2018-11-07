"""
processCheckIns.py
------------------
Author: Thawsitt Naing
Date created: 11/04/2018

Input: Foursquare "checkins" dataset
Output: Text file with user_id and venue_id columns e.g. "11234 3435322"

Notes:
- max_user_id is added to venue ids to eliminate overlap between user and venue ids.
- Tested with Python 2.7
"""
# Number of unique users: 485381
# Number of unique venues: 83999
# Max user id: 2153502
# Min venue id: 2153503


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
            users.add(user_id)
            venues.add(venue_id)
            user_venue_pairs.append((user_id, venue_id))
    print_metrics(users, venues)
    assert(len(users.intersection(venues)) == 0)
    return user_venue_pairs


def write_output_files(user_venue_pairs, percent_train, output_filenames):
    train, test = output_filenames
    total_pairs = len(user_venue_pairs)
    training_set_cutoff = int(total_pairs * percent_train)
    with open(train, 'w') as training_set, open(test, 'w') as test_set:
        for i, pair in enumerate(user_venue_pairs):
            user_id, venue_id = pair
            if i < training_set_cutoff:
                training_set.write('{}\t{}\n'.format(user_id, venue_id))
            else:
                test_set.write('{}\t{}\n'.format(user_id, venue_id))


def print_metrics(users, venues):
    print('Number of unique users: {}'.format(len(users)))
    print('Number of unique venues: {}'.format(len(venues)))
    print('User id range: {} to {}'.format(min(users), max(users)))
    print('Venue id range: {} to {}'.format(min(venues), max(venues)))


def main():
    max_user_id = 2153502 # pre-computed
    input_filename = 'umn_foursquare_datasets/checkins.dat'
    output_train = 'umn_foursquare_datasets/train.txt'
    output_test = 'umn_foursquare_datasets/test.txt'

    user_venue_pairs = read_input(input_filename, max_user_id)
    write_output_files(user_venue_pairs, 0.5, (output_train, output_test))


if __name__ == '__main__':
    main()
