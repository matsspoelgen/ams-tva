import sys
from typing import Dict, List
from collusion import get_collusion_tva_result
from schemes import plurality
from tva_io import read_preferences, scheme_by_name, write_to_output
from tva_types import Scheme, VoteProps
from voting import get_basic_tva_result

def main(schemes: Dict[str, Scheme], collusion_groups: List[List[int]], input_file: str, output_file: str, runoff_output_file: str = "runoff_output.json", runoff_election : int = 0) -> None:
    preferences = read_preferences(input_file)

    original_preferences = preferences.copy()
    # if runoff_election > 1:
    #     basic_tva_result, result = get_first_round_basic_tva_result(preferences, schemes, runoff=runoff_election)
    #     write_to_output(basic_tva_result, runoff_output_file)
    #     for pref in preferences:
    #         temp = []
    #         for val in pref:
    #             if val in result:
    #                 temp.append(val)
    #         preferences[preferences.index(pref)] = temp

    # Performs tva for non strategic first round
    if runoff_election > 0:
        basic_tva_result = get_basic_tva_result(preferences, schemes, real_prefs=original_preferences)
    else:
        basic_tva_result = get_basic_tva_result(preferences, schemes, real_prefs=original_preferences)
    write_to_output(basic_tva_result, output_file)

    #TODO: fix happiness calculation for collusion
    #collusion tva
    # collusion_tva_result = get_collusion_tva_result(preferences, schemes, collusion_groups)
    # write_to_output(collusion_tva_result, output_file)

if __name__ == "__main__":
    input_file = 'preferences.csv'
    output_file = None
    output_file = 'output.json'
    scheme_names = ["plurality", "voting_for_two", "borda", "anti_plurality"]
    collusion_groups = [[0, 3],[2],[1],[4]]   

    # Set voting schemes
    schemes: Dict[str, Scheme] = {}
    scheme_names = scheme_names
    for scheme_name in scheme_names:
        scheme = scheme_by_name(scheme_name)
        if scheme == None:
            print("Invalid voting scheme:", scheme_name)
            sys.exit(1)
        schemes[scheme_name] = scheme
    print("Voting schemes:", scheme_names)

    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <input_file.csv>")
    #     sys.exit(1)
    # input_file = sys.argv[1]
    # output_file = sys.argv[2]

    main(schemes, collusion_groups, input_file, output_file)
