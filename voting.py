from random import randrange
from itertools import permutations
from typing import Dict, List
from tva_types import SystemPreferences, Scheme, VotingOption

def happiness(original_prefs: SystemPreferences, outcome: str) -> List[float]:
    """ Calculate the happiness levels for each voter based on the outcome. """
    # The happiness level is the position of the outcome in the preference list
    happiness_levels = []
    for pref in original_prefs:
        happiness_level = 1 - (pref.index(outcome) / (len(pref) - 1))
        happiness_levels.append(happiness_level)
    return happiness_levels

def alternate_happiness(preferences, outcome, variant, acceptance=1, happiness_ranks=[1, 0.9, 0.7, 0.4, 0.15, 0.05]):
    #Temporary method as a storage for different happiness functions
    happiness_levels = []
    if variant == 0: #Squared positional happiness
        for pref in preferences:
            happiness_level = (len(pref) - pref.index(outcome) - 1)**2
            happiness_levels.append(happiness_level)
    elif variant == 1: #Full happiness when outcome in first n else zero
        for pref in preferences:
            if outcome in pref[0:acceptance]:
                happiness_level = len(pref) - 1
            else:
                happiness_level = 0
            happiness_levels.append(happiness_level)
    elif variant == 2: #Full happiness when outcome not in last n else zero
        for pref in preferences:
            if outcome in pref[-acceptance:]:
                happiness_level = 0
            else:
                happiness_level = (len(pref) - 1) ** 2
            happiness_levels.append(happiness_level)
    elif variant == 3: #Full happiness when outcome in first n else positional happiness
        for pref in preferences:
            if outcome in pref[0:acceptance]:
                happiness_level = (len(pref) - 1) ** 2
            else:
                happiness_level = len(pref) - pref.index(outcome) - 1
            happiness_levels.append(happiness_level)
    elif variant == 4: #Happiness based on ranks when in first 6 else 0
        for pref in preferences:
            if outcome in pref[0:6]:
                happiness_level = (happiness_ranks[pref.index(outcome)] * len(pref)-1)**2 #squared to be more in line with other variants
            else:
                happiness_level = 0
            happiness_levels.append(happiness_level)
    elif variant == 5: #random varient from the previouse 5
        for pref in preferences:
            happiness_level = alternate_happiness([pref], outcome, randrange(5), acceptance, happiness_ranks)[0]
            happiness_levels.append(happiness_level)
    return happiness_levels

def get_vote_result(modified_prefs: SystemPreferences, original_prefs: SystemPreferences, scheme: Scheme, get_full_outcome: bool = False) -> tuple[str, List[float]]:
    """ Calculate the outcome and happiness levels for a given voting scheme and set of preferences. """

    outcome , full_outcome= scheme(modified_prefs)
    happiness_levels = happiness(original_prefs, outcome)

    if get_full_outcome:
        return outcome, happiness_levels, full_outcome
    return outcome, happiness_levels

def get_strategic_options_for_voter(original_system_prefs: SystemPreferences, voter_index: int, scheme: Scheme, full_outcome: list[str] = [], runoff: int = 0) -> List[VotingOption]:
    """ Find strategic voting options for a given voter and voting scheme. """

    voter_original_prefs = original_system_prefs[voter_index]
    voter_pref_permutations = list(permutations(voter_original_prefs))
    strategic_voting_options: List[VotingOption] = []
    suboptimal_strategic_voting_options: List[VotingOption] = []

    # Iterate through all permutations of the voter's preferences
    for i, permutation in enumerate(voter_pref_permutations):
        voter_prefs = list(permutation)

        # Update the system preferences (modified copy)
        modified_system_prefs = [original_voter_prefs if voter_index != i else voter_prefs for i, original_voter_prefs in enumerate(original_system_prefs)]

        # Calculate results for the current permutation
        if runoff > 0:
            outcome, happiness_levels, new_full_outcome = get_vote_result(modified_system_prefs, original_system_prefs, scheme, True)
            voter_happiness = alternate_happiness(original_system_prefs, outcome, 1, runoff)
        else:
            outcome, happiness_levels = get_vote_result(modified_system_prefs, original_system_prefs, scheme)
            voter_happiness = happiness_levels[voter_index]
        overall_happiness: float = sum(happiness_levels)

        if i == 0: # Remebmer the first (original) permutation's results
            true_voter_happiness = voter_happiness
            true_overall_happiness = overall_happiness

        # print(f"Permutation {i+1}: Outcome: {outcome}, Happiness levels: {happiness_levels}")

        # Store strategic voting options
        is_strategic = voter_happiness > true_voter_happiness

        if not is_strategic :
            continue

        voting_option = VotingOption(voter_prefs, outcome, voter_happiness, true_voter_happiness, overall_happiness, true_overall_happiness)
        if runoff > 0:
            suboptimal_strategic_voting_options.append(voting_option)
            if new_full_outcome[1] not in full_outcome[:2]:
                strategic_voting_options.append(voting_option)
        else:
            strategic_voting_options.append(voting_option)

    # If no strategic options were found, return the suboptimal options
    if not strategic_voting_options:
        strategic_voting_options = suboptimal_strategic_voting_options.copy()

    return strategic_voting_options

def get_basic_tva_result(original_system_prefs: SystemPreferences, schemes: Dict[str, Scheme], runoff: int = 0) -> dict:
    """ Calculate the basic TVA result for a given voting scheme and set of preferences. """

    num_voters = len(original_system_prefs)

    basic_tva_result = {}
    for scheme_name, scheme in schemes.items():
        if runoff > 0:
            non_strategic_outcome, non_strategic_happiness_levels, non_strategic_full_outcome = get_vote_result(original_system_prefs, original_system_prefs, scheme, True)
        else:
            non_strategic_outcome, non_strategic_happiness_levels = get_vote_result(original_system_prefs, original_system_prefs, scheme)

        scheme_result = {}
        scheme_result["non_strategic_outcome"] = non_strategic_outcome
        scheme_result["non_strategic_happiness_levels"] = non_strategic_happiness_levels
        scheme_result["non_strategic_overall_happiness"] = sum(non_strategic_happiness_levels)
        scheme_result["voters"] = []

        num_strategic_voters = 0
        for voter_index in range(num_voters):
            if runoff > 0:
                strategic_voting_options = get_strategic_options_for_voter(original_system_prefs, voter_index, scheme, non_strategic_full_outcome, runoff)
            else:
                strategic_voting_options = get_strategic_options_for_voter(original_system_prefs, voter_index, scheme)
            if len(strategic_voting_options) >= 1:
                num_strategic_voters += 1
            scheme_result["voters"].append(strategic_voting_options)

        scheme_result["strategic_voting_risk"] = get_strategic_voting_risk(num_strategic_voters, num_voters)
        basic_tva_result[scheme_name] = scheme_result

    if runoff > 0:
        return basic_tva_result, non_strategic_full_outcome
    return basic_tva_result


def get_strategic_voting_risk(num_strategic_voters: int, num_voters: int) -> float:
    """ Ratio of voters with strategic options to all voters. """

    return num_strategic_voters / num_voters

