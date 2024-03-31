import json
import sys
from typing import List, Dict
import pandas as pd

from schemes import anti_plurality, borda, plurality, voting_for_two
from tva_types import Scheme, SystemPreferences
import argparse

def parse_groups(groups_str: str, voters: List[int]) -> List[List[int]]:
    """ Parse and validate collusion groups. """

    deserialized_groups = json.loads(groups_str.replace('\'', '"'))
    all_voters = voters
    available_voters = voters.copy()

    groups = []
    for group_to_parse in deserialized_groups:
        if not isinstance(group_to_parse, list):
            print("Invalid group:", group, "Groups must be lists.")
            sys.exit(1)

        group = []
        for voter in group_to_parse:
            if not isinstance(voter, int):
                print("Invalid voter:", voter, "Voters must be integers.")
                sys.exit(1)

            if voter not in all_voters:
                print("Unavailable voter:", voter)
                sys.exit(1)

            if voter not in available_voters:
                print("Voter", voter, "is in multiple groups.")
                sys.exit(1)
            
            available_voters.remove(voter)
            group.append(voter)

        if len(group) > 0:
            groups.append(group)

    # Add remaining voters to their own groups
    for voter in available_voters:
        groups.append([voter])

    return groups

def parse_scheme_names(scheme_names: List[str]):
    """ Parse and validate voting schemes. """

    schemes: Dict[str, Scheme] = {}
    for scheme_name in scheme_names:
        scheme = scheme_by_name(scheme_name)
        if scheme == None:
            print("Invalid voting scheme:", scheme_name)
            sys.exit(1)
        schemes[scheme_name] = scheme
    return schemes

def parse_prefs(filename: str) -> SystemPreferences:
    """ Parses and validates preferences from a CSV file."""

    input_df = pd.read_csv(filename, header=None)

    input_df = input_df.transpose()
    removed_voters = []

    for i in range(input_df.shape[0]):
        pref = input_df.iloc[i].dropna().tolist()
        is_valid = True

        # check for duplicate or missing candidates
        if len(pref) != len(set(pref)):
            removed_voters.append(i+1)
            input_df.drop(i, inplace=True)
            is_valid = False

        # candidate names must be single characters
        for candidate in pref:
            if not candidate.isalpha() or len(candidate) > 1:
                removed_voters.append(i+1)
                input_df.drop(i, inplace=True)
                is_valid = False
                break

        if is_valid:
            input_df.iloc[i] = pref

    if removed_voters:
        print("Discarded invalid voters:", removed_voters)

    return input_df.values.tolist()

def scheme_by_name(scheme_name: str) -> Scheme:
    """ Maps a string to a voting scheme. """

    schemes = {
        'plurality': plurality,
        'voting_for_two': voting_for_two,
        'anti_plurality': anti_plurality,
        'borda': borda
    }
    return schemes[scheme_name] if scheme_name in schemes else None

def parse_args():
    """ Parse command line arguments. """

    parser = argparse.ArgumentParser(description="Calculate TVA results for a set of preferences.")
    
    # Positional argument
    parser.add_argument('input', type=str, help='Input file name.')

    # String list argument
    parser.add_argument('-s', '--schemes', nargs='+', type=str, help='List of voting schemes.', default=['plurality', 'voting_for_two', 'borda', 'anti_plurality'])
    
    # Nested list argument. This will require custom parsing because argparse does not directly support nested lists.
    parser.add_argument('-g', '--groups', type=str, help='Nested list of collusion groups.')
    
    # Single string argument
    parser.add_argument('-o', '--output', type=str, help='Output file name.')
    
    args = parser.parse_args()

    # Read preferences from input file
    system_preferences = parse_prefs(args.input)

    # Set voting schemes
    schemes: List[Scheme] = parse_scheme_names(args.schemes)
    print("Voting schemes:", ", ".join(args.schemes))

    # Custom parsing for the nested list
    groups: List[List[int]] = parse_groups(args.groups, list(range(len(system_preferences)))) if args.groups else []
    print("Collusion groups:", groups)
    
    return system_preferences, schemes, groups, args.output

def tva_result_to_json(basic_tva_result) -> str:
    """ Convert TVA result to a JSON string. """
    return json.dumps(basic_tva_result, indent=4, default=generic_serializer)

def generic_serializer(obj):
    """A generic JSON serializer for objects not serializable by default json code"""
    if hasattr(obj, "__dict__"):
        # Serialize objects by turning their __dict__ property into a dict.
        # This works for most custom classes.
        return obj.__dict__
    elif isinstance(obj, set):
        # Example: Convert sets to lists
        return list(obj)
    # Add more checks here for other types if necessary.
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def write_to_output(basic_tva_result, output_file=None):
    """ Write to output file or print to console if no output file is specified. """
    if output_file:
        with open(output_file, "w") as file:
            file.write(tva_result_to_json(basic_tva_result))
            print("Results written to", output_file)
    else:
        print(tva_result_to_json(basic_tva_result))