from collections import Counter
from random import randrange

def plurality(preferences):
    votes = [pref[0] for pref in preferences]
    outcome = Counter(votes).most_common()
    outcome.sort(key=lambda x: (-x[1], x[0]))
    return outcome[0][0]

def voting_for_two(preferences):
    votes = [pref[0] for pref in preferences] + [pref[1] for pref in preferences]
    outcome = Counter(votes).most_common()
    outcome.sort(key=lambda x: (-x[1], x[0]))
    return outcome[0][0]

def anti_plurality(preferences, candidates):
    # Count the number of times each candidate is placed last
    last_place_votes = Counter(pref[-1] for pref in preferences)

    # Calculate the score for each candidate by subtracting the number of last place votes from the total votes
    scores = {candidate: 0 for candidate in candidates}
    total_votes = len(preferences)
    for candidate in scores:
        scores[candidate] = total_votes - last_place_votes.get(candidate, 0)

    outcome = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return outcome[0][0]

def borda(preferences, candidates):
    scores = {candidate: 0 for candidate in candidates}
    for pref in preferences:
        for i, candidate in enumerate(pref):
            # Assign points based on the position in the preference list
            scores[candidate] += len(candidates) - i - 1
    outcome = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return outcome[0][0]

def happiness(preferences, outcome):
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
                happiness_level = (len(pref) - 1) ** 2
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



def analyze_scheme_for_voter(preferences, voter, scheme):
    print(f"Analyzing {scheme}-scheme for voter {voter}...")
    print('unimplemented')
