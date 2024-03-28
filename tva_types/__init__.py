from typing import Callable, List

VoterPreferences = List[str]
""" Candidates in order of preference. """

SystemPreferences = List[VoterPreferences]
""" All voter preferences. """

Scheme = Callable[[SystemPreferences], str]
""" Function that takes all voter preferences and returns the winner of the vote. """