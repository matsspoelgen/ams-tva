import json
import pandas as pd

from schemes import anti_plurality, borda, plurality, voting_for_two
from tva_types import Scheme


def read_preferences(filename):
    input_df = pd.read_csv(filename, header=None)

    # first row contains the voting scheme
    scheme_name = input_df.iloc[0, 0]
    input_df.drop(0, inplace=True)

    input_df = input_df.transpose()
    removed_voters = []

    for i in range(input_df.shape[0]):
        pref = input_df.iloc[i].dropna().tolist()
        if len(pref) != len(set(pref)):
            removed_voters.append(i)
            input_df.drop(i, inplace=True)
        else:
            input_df.iloc[i] = pref

    if removed_voters:
        print("Discarded invalid voters:", removed_voters)

    return scheme_name, input_df.values.tolist()

def scheme_by_name(scheme_name) -> Scheme:
    schemes = {
        'plurality': plurality,
        'voting_for_two': voting_for_two,
        'anti_plurality': anti_plurality,
        'borda': borda
    }
    return schemes[scheme_name] if scheme_name in schemes else None

def basic_tva_result_to_json(basic_tva_result) -> str:
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
            file.write(basic_tva_result_to_json(basic_tva_result))
            print("Results written to", output_file)
    else:
        print(basic_tva_result_to_json(basic_tva_result))