from tva_types import VoterPreferences

class VotingOption:
    def __init__(self, preference_list: VoterPreferences, voting_outcome: str, voter_happiness: float, overall_happiness: float, true_overall_happiness: float):
        self.modified_preference_list: VoterPreferences = preference_list  # 𝑣̃𝑖𝑗
        self.voting_outcome: str = voting_outcome  # 𝑂̃
        self.voter_happiness: float = voter_happiness  # ̃𝐻𝑖
        self.overall_happiness: float = overall_happiness  # 𝐻̃
        self.true_overall_happiness: float = true_overall_happiness  # 𝐻

    def __str__(self) -> str:
        return f"VotingOption(preferences={self.modified_preference_list}, outcome={self.voting_outcome}, happiness={self.voter_happiness}, o_happiness={self.overall_happiness}, t_o_happiness={self.true_overall_happiness})"
