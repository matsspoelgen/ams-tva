import sys
from tva_io import read_preferences, scheme_by_name, write_to_output
from voting import  get_basic_tva_result

def main(input_file: str, output_file: str):
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

    basic_tva_result = get_basic_tva_result(preferences, scheme)
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
