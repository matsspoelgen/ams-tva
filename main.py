import csv
import sys
from voting import plurality, voting_for_two, anti_plurality, borda, happiness
import pandas as pd

def read_preferences(filename):
    input_df = pd.read_csv(filename, header=None)

    # first row contains the voting scheme
    scheme = input_df.iloc[0, 0]
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

    return scheme, input_df.values.tolist()

def main(filename):
    scheme, preferences = read_preferences(filename)
    candidates = set(preferences[0])
    
    print("Plurality Voting Outcome:", plurality(preferences))
    print("Voting for Two Outcome:", voting_for_two(preferences))
    print("Anti-Plurality Voting Outcome:", anti_plurality(preferences, candidates))
    borda_outcome = borda(preferences, candidates)
    print("Borda Voting Outcome:", borda_outcome)
    print("Happiness Levels (Borda):", happiness(preferences, borda_outcome))

if __name__ == "__main__":
    filename = 'preferences.csv'
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <input_file.csv>")
    #     sys.exit(1)
    # filename = sys.argv[1]
    main(filename)
