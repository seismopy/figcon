"""
A relatively simple sconfig for testing options hierarchy.
"""

from types import SimpleNamespace

something_new = 1

# this should update base snuffler configs
snuffler = SimpleNamespace(box_alpha=84, full_screen=True, another_new_thing="who")


# This should also update catalog


class catalog:
    agency = "MIRARCO"
    time_before_pick = 22
    more_new = "major tom"
    tibble = SimpleNamespace(old=True)

    class Dribble:  # this is just getting crazy
        out = 1
