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

generate_preferences_csv(10, 3, "exp_preferences.csv")

main.main(['plurality', 'voting_for_two', 'borda', 'anti_plurality'], "exp_preferences.csv", "exp_output.json")
print(get_happiness_by_scheme(read_output("exp_output.json"), "plurality"))
print(get_risk_by_scheme(read_output("exp_output.json"), "plurality"))
print(calculate_average_happiness_increase_by_scheme(read_output("exp_output.json"), "plurality"))
plot_strategic_voting_risk(read_output("exp_output.json"))

