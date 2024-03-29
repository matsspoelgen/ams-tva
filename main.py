import sys
from tva_io import read_preferences, scheme_by_name, write_to_output
from voting import  get_basic_tva_result, get_first_round_basic_tva_result

def main(input_file: str, output_file: str, runoff_output_file: str = "runoff_output.json", runoff_election : int =0) -> None:
    scheme_name, preferences = read_preferences(input_file)

    # Set voting scheme
    scheme = scheme_by_name(scheme_name)
    if scheme == None:
        print("Invalid voting scheme:", scheme_name)
        sys.exit(1)
    print("Voting scheme:", scheme_name)

    # voter = 0
    # print("Voter", voter)
    # voting_options: List[VotingOption] = get_strategic_options_for_voter(preferences, voter, scheme)
    # print("Strategic options:")
    # print(',\n'.join([str(option) for option in voting_options]))

    original_preferences = preferences.copy()
    if runoff_election > 1:
        result = ["B", "C"]
        basic_tva_result, result = get_first_round_basic_tva_result(preferences, scheme, runoff=runoff_election)
        write_to_output(basic_tva_result, runoff_output_file)
        for pref in preferences:
            temp = []
            for val in pref:
                if val in result:
                    temp.append(val)
            preferences[preferences.index(pref)] = temp


    #Performs tva for non strategic first round
    basic_tva_result = get_basic_tva_result(preferences, scheme, real_prefs=original_preferences)
    write_to_output(basic_tva_result, output_file)

if __name__ == "__main__":
    input_file = 'preferences.csv'
    output_file = None
    output_file = 'output.json'

    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <input_file.csv>")
    #     sys.exit(1)
    # input_file = sys.argv[1]
    # output_file = sys.argv[2]
    main(input_file, output_file)
