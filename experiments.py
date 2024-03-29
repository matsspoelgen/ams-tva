import csv
import json
import random
import main
import matplotlib.pyplot as plt


random.seed(42)
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

def get_happiness_by_scheme(output: dict, scheme: str) -> float:
    return output[scheme]["non_strategic_overall_happiness"]

def get_risk_by_scheme(output: dict, scheme: str) -> float:
    return output[scheme]["strategic_voting_risk"]

def calculate_average_happiness_increase_by_scheme(data, scheme):
    total_increase = 0
    voters_count = 0

    for voter_data in data[scheme]['voters'][0]:  # Assuming the first list contains relevant voter data
        increase = voter_data['voter_happiness'] - voter_data['true_voter_happiness']
        total_increase += increase
        voters_count += 1

    return total_increase / voters_count if voters_count > 0 else 0

def plot_strategic_voting_risk(data):
    risks = [details['strategic_voting_risk'] for scheme, details in data.items() if 'strategic_voting_risk' in details]
    schemes = [scheme for scheme in data if 'strategic_voting_risk' in data[scheme]]

    plt.bar(schemes, risks, color='skyblue')
    plt.xlabel('Voting Scheme')
    plt.ylabel('Strategic Voting Risk')
    plt.title('Strategic Voting Risk by Voting Scheme')
    plt.xticks(rotation=45)
    plt.show()


def run_experiment(candidate_numbers, voter_numbers):
    results = {}
    for num_voters in voter_numbers:
        happiness_data = []
        risk_data = []
        avg_increase_data = []
        for num_candidates in candidate_numbers:
            # Generate preferences CSV
            filename = f"exp_preferences.csv"
            generate_preferences_csv(num_voters, num_candidates, filename)

            # Run analysis and read output
            output_filename = f"exp_output.json"
            main.main(["plurality", "voting_for_two", "borda", "anti_plurality"], filename, output_filename)
            output = read_output(output_filename)

            # Collect metrics for "plurality" scheme as an example
            happiness = get_happiness_by_scheme(output, "plurality")
            risk = get_risk_by_scheme(output, "plurality")
            avg_increase = calculate_average_happiness_increase_by_scheme(output, "plurality")

            happiness_data.append(happiness)
            risk_data.append(risk)
            avg_increase_data.append(avg_increase)

        # Store results for current voter number
        results[num_voters] = {
            "happiness": happiness_data,
            "risk": risk_data,
            "avg_increase": avg_increase_data
        }

    return results


def plot_combined_metrics(candidate_numbers, results):
    fig, axs = plt.subplots(len(results), 3, figsize=(15, len(results) * 5))

    for idx, (num_voters, metrics) in enumerate(results.items()):
        axs[idx, 0].plot(candidate_numbers, metrics["happiness"], marker='o', linestyle='-', color='blue')
        axs[idx, 0].set_title(f'Non-Strategic Overall Happiness (Voters={num_voters})')
        axs[idx, 0].set_xlabel('Number of Candidates')
        axs[idx, 0].set_ylabel('Happiness')

        axs[idx, 1].plot(candidate_numbers, metrics["risk"], marker='o', linestyle='-', color='red')
        axs[idx, 1].set_title(f'Strategic Voting Risk (Voters={num_voters})')
        axs[idx, 1].set_xlabel('Number of Candidates')
        axs[idx, 1].set_ylabel('Risk')

        axs[idx, 2].plot(candidate_numbers, metrics["avg_increase"], marker='o', linestyle='-', color='green')
        axs[idx, 2].set_title(f'Average Happiness Increase (Voters={num_voters})')
        axs[idx, 2].set_xlabel('Number of Candidates')
        axs[idx, 2].set_ylabel('Happiness Increase')

    plt.tight_layout()
    plt.show()


generate_preferences_csv(10, 3, "exp_preferences.csv")

main.main(['plurality', 'voting_for_two', 'borda', 'anti_plurality'], "exp_preferences.csv", "exp_output.json")
print(get_happiness_by_scheme(read_output("exp_output.json"), "plurality"))
print(get_risk_by_scheme(read_output("exp_output.json"), "plurality"))
print(calculate_average_happiness_increase_by_scheme(read_output("exp_output.json"), "plurality"))
plot_strategic_voting_risk(read_output("exp_output.json"))

candidate_numbers = [3, 4, 5, 6]  # Range of candidate numbers to test
voter_numbers = [10, 50, 100]  # Range of voter numbers to test

results = run_experiment(candidate_numbers, voter_numbers)
plot_combined_metrics(candidate_numbers, results)