import csv
import json
import random
import main

def generate_preferences_csv(num_voters: int, num_candidates: int, filename: str) -> None:
    candidates = [chr(65 + i) for i in range(num_candidates)]  # Candidate labels A, B, C, ...
    preferences = []
    for _ in range(num_voters):
        column = random.sample(candidates, num_candidates)
        preferences.append(column)
    preferences = list(zip(*preferences))  # Transpose the list to have each row represent a voter
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for preference in preferences:
            writer.writerow(preference)

def read_output(filename: str) -> dict:
    with open(filename, 'r') as file:
        return json.load(file)

generate_preferences_csv(5, 3, "exp_preferences.csv")

main.main(['plurality', 'voting_for_two', 'borda', 'anti_plurality'], "exp_preferences.csv", "exp_output.json")
