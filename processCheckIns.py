"""
processCheckIns.py
------------------
Author: Thawsitt Naing
Date created: 11/04/2018

Input: Foursquare "checkins" dataset
Output: Text file with user_id and venue_id columns e.g. "11234 3435322"
Note: max_user_id is added to venue ids to eliminate overlap between user and venue ids. 
"""
# Number of unique users: 485381
# Number of unique venues: 83999
# Max user id: 2153502
# Min venue id: 2153503

def processCheckins(max_user_id):
    input_filename = 'umn_foursquare_datasets/checkins.dat'
    output_filename = 'umn_foursquare_datasets/checkins.txt'
    users, venues = set(), set()

    with open(input_filename, 'r') as input, open(output_filename, 'w') as output:
        for i, line in enumerate(input):
            if i > 1:
                parsed = [str.strip() for str in line.split('|')]
                if len(parsed) < 6:
                    print('skipped: {}'.format(parsed))
                    continue
                user_id = int(parsed[1])
                venue_id = int(parsed[2]) + max_user_id
                users.add(user_id)
                venues.add(venue_id)
                output.write('{}\t{}\n'.format(user_id, venue_id))

    print('Number of unique users: {}'.format(len(users)))
    print('Number of unique venues: {}'.format(len(venues)))
    print('Max user id: {}'.format(max(users)))
    print('Min venue id: {}'.format(min(venues)))
    assert(len(users.intersection(venues)) == 0)


def main():
    max_user_id = 2153502
    processCheckins(max_user_id)


if __name__ == '__main__':
    main()
