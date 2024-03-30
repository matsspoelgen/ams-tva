from itertools import permutations
from typing import Dict, List

import pandas as pd
from tva_types import Scheme, SystemPreferences, VotingOption
from voting import get_strategic_voting_risk, get_vote_result


def get_strategic_options_for_group(system_preferences: SystemPreferences, scheme: Scheme, collusion_group: List[int]) -> List[VotingOption]:
    # calculate true group happiness
    true_outcome, true_happiness_levels = get_vote_result(system_preferences, scheme)
    return get_strategic_options_for_group_rek(system_preferences, true_happiness_levels, scheme, collusion_group, 0)


def get_strategic_options_for_group_rek(system_preferences: SystemPreferences, true_happiness_levels: List[float], scheme: Scheme, collusion_group: List[int], depth: int, full_outcome: list[str] = [], runoff: int = 0, real_prefs: SystemPreferences = []) -> List[VotingOption]:

    # the next voter is always first in the list
    voter_index = collusion_group[depth]
    voter_original_prefs = system_preferences[voter_index]
    voter_pref_permutations = list(permutations(voter_original_prefs))
    strategic_voting_options: List[List[VotingOption]] = []

    # iterate through all permutations of this voter
    for i, permutation in enumerate(voter_pref_permutations):

        # update the system preferences
        voter_prefs = list(permutation)
        system_preferences[voter_index] = voter_prefs

        if depth == len(collusion_group) - 1:

            # calculate the results for the current permutation
            outcome, happiness_levels = get_vote_result(system_preferences, scheme)

            # check if the collusion group has higher overall happiness
            group_happiness = sum(happiness_levels[voter_index] for voter_index in collusion_group)
            true_group_happiness = sum(true_happiness_levels[voter_index] for voter_index in collusion_group)
            better_overall = group_happiness > true_group_happiness
            if (not better_overall):
                continue

            # check if anyone in the collusion group has individual lower happiness
            anyone_unhappy = any(happiness_levels[voter_index] < true_happiness_levels[voter_index] for voter_index in collusion_group)
            if (anyone_unhappy):
                continue

            # store the strategic voting options
            strategic_voting_options.append([VotingOption(voter_prefs, outcome, happiness_levels[voter_index], true_happiness_levels[voter_index], group_happiness, true_group_happiness) for voter_index in collusion_group])
        else:
            # recursively call the function for the next voter in the collusion group
            strategic_voting_options.extend(get_strategic_options_for_group_rek(system_preferences, true_happiness_levels, scheme, collusion_group, depth + 1, full_outcome, runoff, real_prefs))

    # restore the original preferences
    system_preferences[voter_index] = voter_original_prefs

    return strategic_voting_options

def get_collusion_tva_result(system_preferences: SystemPreferences, schemes: Dict[str, Scheme], collusion_groups: List[List[int]]) -> dict:
    """ Calculate the basic TVA result for a given voting scheme and set of preferences. """

    num_voters = len(system_preferences)
    num_groups = len(collusion_groups)
    num_candidates = len(system_preferences[0])

    collusion_tva_result = {}
    for scheme_name, scheme in schemes.items():
        non_strategic_outcome, non_strategic_happiness_levels = get_vote_result(system_preferences, scheme)

        scheme_result = {}
        scheme_result["non_strategic_outcome"] = non_strategic_outcome
        scheme_result["non_strategic_happiness_levels"] = non_strategic_happiness_levels
        scheme_result["non_strategic_overall_happiness"] = sum(non_strategic_happiness_levels)
        scheme_result["voters"] = []

        num_strategic_options = 0
        strategic_options_dict: Dict[int, List[VotingOption]] = {}
        for group_index in range(num_groups):
            collusion_group = collusion_groups[group_index]
            strategic_group_voting_options = get_strategic_options_for_group(system_preferences, scheme, collusion_group)
            num_strategic_options += len(collusion_group) * len(strategic_group_voting_options)                                     # TODO remove with new risk function

            # options for groups are stored in rows so this is ugly af
            options_df = pd.DataFrame(strategic_group_voting_options)
            for index in range(len(collusion_group)):
                strategic_options_dict[collusion_group[index]] = options_df[index].tolist() if options_df.shape[1] > 0 else []

        # sorted voters by key
        scheme_result["voters"] = [strategic_options_dict[voter_index] for voter_index in range(num_voters)]
        scheme_result["strategic_voting_risk"] = get_strategic_voting_risk(num_strategic_options, num_groups, num_candidates)       # TODO change with new risk function
        collusion_tva_result[scheme_name] = scheme_result

    return collusion_tva_result