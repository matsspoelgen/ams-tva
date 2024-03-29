from random import randrange
from itertools import permutations
from typing import List
from tva_types import SystemPreferences, Scheme, VotingOption
import math

def happiness(preferences: SystemPreferences, outcome: str) -> List[float]:
    """ Calculate the happiness levels for each voter based on the outcome. """
    # The happiness level is the position of the outcome in the preference list
    happiness_levels = []
    for pref in preferences:
        happiness_level = len(pref) - pref.index(outcome) - 1
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


def get_vote_result(preferences: SystemPreferences, scheme: Scheme, real_prefs: SystemPreferences =[], get_full_outcome: bool = False) -> tuple[str, List[float]]:
    """ Calculate the outcome and happiness levels for a given voting scheme and set of preferences. """
    outcome , full_outcome= scheme(preferences)
    if real_prefs:
        happiness_levels = happiness(real_prefs, outcome)
    else:
        happiness_levels = happiness(preferences, outcome)
    if get_full_outcome:
        return outcome, happiness_levels, full_outcome
    return outcome, happiness_levels

def get_strategic_options_for_voter(system_preferences: SystemPreferences, voter_index: int, scheme: Scheme, full_outcome: list[str] = [], runoff: int = 0, real_prefs: SystemPreferences = []) -> List[VotingOption]:
    """ Find strategic voting options for a given voter and voting scheme. """

    voter_original_prefs = system_preferences[voter_index]
    voter_pref_permutations = list(permutations(voter_original_prefs))
    strategic_voting_options: List[VotingOption] = []
    suboptimal_strategic_voting_options: List[VotingOption] = []

    # Iterate through all permutations of the voter's preferences
    for i, permutation in enumerate(voter_pref_permutations):
        voter_prefs = list(permutation)
        system_preferences[voter_index] = voter_prefs

        # Calculate results for the current permutation
        if runoff > 0:
            outcome, happiness_levels, new_full_outcome = get_vote_result(system_preferences, scheme, real_prefs, True)
            voter_happiness = alternate_happiness(system_preferences, outcome, 1, runoff)
        else:
            outcome, happiness_levels = get_vote_result(system_preferences, scheme, real_prefs)
            voter_happiness = happiness_levels[voter_index]
        overall_happiness: float = sum(happiness_levels)

        if i == 0: # Remebmer the first (original) permutation's results
            true_voter_happiness = voter_happiness
            true_overall_happiness = overall_happiness

        # print(f"Permutation {i+1}: Outcome: {outcome}, Happiness levels: {happiness_levels}")

        # Store strategic voting options
        is_strategic = voter_happiness > true_voter_happiness
        if runoff > 0:
            if is_strategic:
                suboptimal_strategic_voting_options.append(VotingOption(voter_prefs, outcome, voter_happiness, true_voter_happiness, overall_happiness, true_overall_happiness))
            if is_strategic and new_full_outcome[1] not in full_outcome[:2]:
                strategic_voting_options.append(VotingOption(voter_prefs, outcome, voter_happiness, true_voter_happiness, overall_happiness, true_overall_happiness))
        else:
            if is_strategic:
                strategic_voting_options.append(VotingOption(voter_prefs, outcome, voter_happiness, true_voter_happiness, overall_happiness, true_overall_happiness))

    # Restore the original preferences
    system_preferences[voter_index] = voter_original_prefs
    return strategic_voting_options


def get_basic_tva_result(system_preferences: SystemPreferences, schemes: Scheme, runoff: int = 0, real_prefs: SystemPreferences = []) -> dict:
    """ Calculate the basic TVA result for a given voting scheme and set of preferences. """

    num_voters = len(system_preferences)
    num_candidates = len(system_preferences[0])

    basic_tva_result = {}
    for scheme_name, scheme in schemes.items():
        if runoff > 0:
            non_strategic_outcome, non_strategic_happiness_levels, non_strategic_full_outcome = get_vote_result(system_preferences, scheme, real_prefs, True)
        else:
            non_strategic_outcome, non_strategic_happiness_levels = get_vote_result(system_preferences, scheme, real_prefs)

        scheme_result = {}
        scheme_result["non_strategic_outcome"] = non_strategic_outcome
        scheme_result["non_strategic_happiness_levels"] = non_strategic_happiness_levels
        scheme_result["non_strategic_overall_happiness"] = sum(non_strategic_happiness_levels)
        scheme_result["voters"] = []

        num_strategic_options = 0
        for voter_index in range(num_voters):
            if runoff > 0:
                strategic_voting_options = get_strategic_options_for_voter(system_preferences, voter_index, scheme, non_strategic_full_outcome, runoff, real_prefs)
            else:
                strategic_voting_options = get_strategic_options_for_voter(system_preferences, voter_index, scheme, real_prefs=real_prefs)
            num_strategic_options += len(strategic_voting_options)
            scheme_result["voters"].append(strategic_voting_options)

        scheme_result["strategic_voting_risk"] = get_strategic_voting_risk(num_strategic_options, num_voters, num_candidates)
        basic_tva_result[scheme_name] = scheme_result

    return basic_tva_result


def get_strategic_voting_risk(num_strategic_options: int, num_voters: int, num_candidates: int) -> float:
    """ Ratio of strategic voting options to the total number of options. """

    permutations_per_voter = math.factorial(num_candidates)
    total_options = permutations_per_voter * num_voters
    return num_strategic_options / total_options
