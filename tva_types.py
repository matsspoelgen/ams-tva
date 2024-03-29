from typing import Callable, List

VoterPreferences = List[str]
""" Candidates in order of preference. """

SystemPreferences = List[VoterPreferences]
""" All voter preferences. """

Scheme = Callable[[SystemPreferences], str]
""" Function that takes all voter preferences and returns the winner of the vote. """

class VotingOption:
    """ A voting option for a voter.
    
    Attributes:
        modified_preference_list:       Alternative to the original preference list for the voter
        voting_outcome:                 Outcome of the alternative voting option
        voter_happiness:                Happiness of the voter with the alternative voting outcome
        true_voter_happiness:           Happiness of the voter with the original voting outcome
        overall_happiness:              Summed happiness of all voters with the alternative voting outcome
        true_overall_happiness:         Summed happiness of all voters with the original voting outcome
    """

    def __init__(self, preference_list: VoterPreferences, voting_outcome: str, voter_happiness: float, true_voter_happiness: float, overall_happiness: float, true_overall_happiness: float):
        self.modified_preference_list: VoterPreferences = preference_list  # 𝑣̃𝑖𝑗
        self.voting_outcome: str = voting_outcome  # 𝑂̃
        self.voter_happiness: float = voter_happiness  # ̃𝐻𝑖
        self.true_voter_happiness: float = true_voter_happiness  # 𝐻𝑖
        self.overall_happiness: float = overall_happiness  # 𝐻̃
        self.true_overall_happiness: float = true_overall_happiness  # 𝐻