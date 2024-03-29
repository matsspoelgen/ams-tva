import csv
import random
import json
import matplotlib.pyplot as plt

from main import main


def generate_random_preferences(num_voters: int, num_candidates: int) -> list:
    candidates = [chr(65 + i) for i in range(num_candidates)]  # Generate candidate names A, B, C, ...
    preferences = [[] for _ in range(num_candidates)]  # List to hold preferences for each candidate

    for _ in range(num_voters):
        voter_pref = random.sample(candidates, len(candidates))
        for idx, candidate in enumerate(voter_pref):
            preferences[idx].append(candidate)

    return preferences


def write_preferences_to_file(preferences: list, file_path: str) -> None:
    """
    Writes the generated random preferences to a CSV file, matching the specified format.

    :param preferences: A list of lists, where each sublist represents the
                        preference list for a candidate across all voters.
    :param file_path: The path to the CSV file where the preferences will be saved.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for preference in preferences:
            writer.writerow(preference)

def read_output(file_path: str) -> dict:
    with open(file_path) as file:
        data = json.load(file)
    return data

def run_experiment_num_voters_candidates(file_path: str, output_file: str, number_voters : int, number_candidates : int) -> dict:
    preferences = generate_random_preferences(number_voters, number_candidates)
    write_preferences_to_file(preferences, file_path)
    main(file_path, output_file)
    return read_output(output_file)

def visualize_results(results: dict):
    # Placeholder for visualization logic
    # This could be adapted based on the structure of your results
    voters = range(len(results["happiness_levels"]))
    happiness_levels = results["happiness_levels"]

    plt.figure(figsize=(10, 6))
    plt.bar(voters, happiness_levels, color='skyblue')
    plt.xlabel('Voter')
    plt.ylabel('Happiness Level')
    plt.title('Voter Happiness Levels After Strategic Voting')
    plt.show()

if __name__ == "__main__":
    file_path = 'experiment.csv'
    output_file = 'output.json'
    print("Running experiment 1: increasing number of voters")
    for num_voters in [5, 10, 20, 50, 100, 200]:
        print(f"Number of voters: {num_voters}")
        results = run_experiment_num_voters_candidates(file_path, output_file, num_voters, 3)

        visualize_results(results)
