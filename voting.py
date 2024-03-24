from collections import Counter

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
        happiness_level = len(pref) - pref.index(outcome)
        happiness_levels.append(happiness_level)
    return happiness_levels