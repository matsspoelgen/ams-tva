import sys
from typing import List
from schemes import anti_plurality, borda, plurality, voting_for_two
from tva_types import Scheme
from voting import get_strategic_options_for_voter
import pandas as pd

from voting_option import VotingOption

def read_preferences(filename):
    input_df = pd.read_csv(filename, header=None)

    # first row contains the voting scheme
    scheme_name = input_df.iloc[0, 0]
    input_df.drop(0, inplace=True)

    input_df = input_df.transpose()
    removed_voters = []

    for i in range(input_df.shape[0]):
        pref = input_df.iloc[i].dropna().tolist()
        if len(pref) != len(set(pref)):
            removed_voters.append(i)
            input_df.drop(i, inplace=True)
        else:
            input_df.iloc[i] = pref

    if removed_voters:
        print("Discarded invalid voters:", removed_voters)

    return scheme_name, input_df.values.tolist()

def scheme_by_name(scheme_name) -> Scheme:
    schemes = {
        'plurality': plurality,
        'voting_for_two': voting_for_two,
        'anti_plurality': anti_plurality,
        'borda': borda
    }

    return schemes[scheme_name] if scheme_name in schemes else None

def main(filename):
    scheme_name, preferences = read_preferences(filename)

    # Set voting scheme
    scheme = scheme_by_name(scheme_name)
    if scheme == None:
        print("Invalid voting scheme:", scheme_name)
        sys.exit(1)
    print("Voting scheme:", scheme_name)
    
    voter = 0
    print("Voter", voter)
    voting_options: List[VotingOption] = get_strategic_options_for_voter(preferences, voter, scheme)
    print("Strategic options:")
    print(',\n'.join([str(option) for option in voting_options]))

if __name__ == "__main__":
    filename = 'preferences.csv'
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <input_file.csv>")
    #     sys.exit(1)
    # filename = sys.argv[1]
    main(filename)
