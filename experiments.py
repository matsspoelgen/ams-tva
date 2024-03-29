import csv
import random
import json
import matplotlib.pyplot as plt

from main import main


def generate_and_write_preferences(num_voters: int, num_candidates: int, file_path: str, voting_scheme: str) -> None:
    """
    Generates random voting preferences and writes them to a CSV file, including the voting scheme type.

    :param num_voters: The number of voters for whom to generate preferences.
    :param num_candidates: The number of candidates to be included in the preferences.
    :param file_path: The path to the CSV file where the preferences will be saved.
    :param voting_scheme: A string representing the voting scheme used.
    """
    candidates = [chr(65 + i) for i in range(num_candidates)]  # Generate candidate names A, B, C, ...
    preferences = [[] for _ in range(num_candidates)]  # List to hold preferences for each candidate

    for _ in range(num_voters):
        voter_pref = random.sample(candidates, len(candidates))
        for idx, candidate in enumerate(voter_pref):
            preferences[idx].append(candidate)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([voting_scheme] + ['null' for _ in range(num_voters - 1)])  # Adjust for your definition of 'null'
        for preference in preferences:
            writer.writerow(preference)  # Then, write the preferences for each candidate

def read_output(file_path: str) -> dict:
    with open(file_path) as file:
        data = json.load(file)
    return data

def run_experiment_num_voters_candidates(file_path: str, output_file: str, number_voters : int, number_candidates : int, voting_scheme : str) -> dict:
    generate_and_write_preferences(number_voters, number_candidates, file_path, voting_scheme)
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
        results = run_experiment_num_voters_candidates(file_path, output_file, num_voters, 3, "plurality")

       # visualize_results(results)
