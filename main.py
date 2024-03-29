import sys
from typing import List
from tva_io import read_preferences, scheme_by_name, write_to_output
from tva_types import Scheme
from voting import  get_basic_tva_result, get_first_round_basic_tva_result

def main(scheme_names: str, input_file: str, output_file: str, runoff_output_file: str = "runoff_output.json", runoff_election : int =0) -> None:
    preferences = read_preferences(input_file)

    # Set voting schemes
    schemes = {}
    for scheme_name in scheme_names:
        scheme = scheme_by_name(scheme_name)
        if scheme == None:
            print("Invalid voting scheme:", scheme_name)
            sys.exit(1)
        schemes[scheme_name] = scheme
    print("Voting schemes:", scheme_names)

    original_preferences = preferences.copy()
    # if runoff_election > 1:
    #     result = ["B", "C"]
    #     basic_tva_result, result = get_first_round_basic_tva_result(preferences, schemes, runoff=runoff_election)
    #     write_to_output(basic_tva_result, runoff_output_file)
    #     for pref in preferences:
    #         temp = []
    #         for val in pref:
    #             if val in result:
    #                 temp.append(val)
    #         preferences[preferences.index(pref)] = temp

    #Performs tva for non strategic first round
    basic_tva_result = get_basic_tva_result(preferences, schemes, real_prefs=original_preferences)
    write_to_output(basic_tva_result, output_file)

if __name__ == "__main__":
    input_file = 'preferences.csv'
    output_file = None
    output_file = 'output.json'
    scheme_names = ['plurality', 'voting_for_two', 'borda', 'anti_plurality']

    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <input_file.csv>")
    #     sys.exit(1)
    # input_file = sys.argv[1]
    # output_file = sys.argv[2]

    main(scheme_names, input_file, output_file)
