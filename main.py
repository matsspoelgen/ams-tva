import csv
import sys
from voting import plurality, voting_for_two, anti_plurality, borda, happiness

def read_preferences(filename):
    preferences = []
    invalid_preferences = []
    row_number = 1
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            row_upper = [item.upper() for item in row]
            if len(row_upper) == len(set(row_upper)) and all(item.isalpha() and len(item) == 1 for item in row_upper):
                preferences.append(row_upper)
            else:
                invalid_preferences.append(row_number)
            row_number += 1
    if invalid_preferences:
        print("Discarded invalid preferences at row(s):", ', '.join(map(str, invalid_preferences)))
    return preferences

def main(filename):
    preferences = read_preferences(filename)
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
