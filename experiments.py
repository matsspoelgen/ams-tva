import csv
import random

def generate_preferences_csv(num_voters: int, num_candidates: int, filename: str) -> None:
    candidates = [chr(65 + i) for i in range(num_candidates)]  # Candidate labels A, B, C, ...
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for _ in range(num_voters):
            preferences = random.sample(candidates, num_candidates)  # Randomly shuffle the candidates
            writer.writerow(preferences)

if __name__ == "__main__":
    num_voters = 4
    num_candidates = 5
    filename = "exp_preferences.csv"
    generate_preferences_csv(num_voters, num_candidates, filename)
