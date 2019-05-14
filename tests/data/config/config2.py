"""
Another simple sconfig.
"""
from types import SimpleNamespace

new_namespace = SimpleNamespace(here="or there")

catalog = SimpleNamespace(
    time_after=100, tibble=SimpleNamespace(orange=True, old=False, fat=True)
)

snuffler = SimpleNamespace(box_alpha=42, new_here_maybe="2", gap_lap_tolerance=100)
