import csv
import random

def generate_preferences_csv(num_voters: int, num_candidates: int, filename: str) -> None:
    candidates = [chr(65 + i) for i in range(num_candidates)]  # Candidate labels A, B, C, ...
    preferences = []
    for _ in range(num_candidates):
        column = random.sample(candidates, num_voters)
        preferences.append(column)
    preferences = list(zip(*preferences))  # Transpose the list to have each row represent a voter
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for preference in preferences:
            writer.writerow(preference)

generate_preferences_csv(4, 5, "example.csv")
