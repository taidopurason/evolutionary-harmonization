from typing import Iterable, List

from mingus.core.chords import from_shorthand


def get_chord_notes(chord: str) -> List[str]:
    return from_shorthand(chord)


def note_match_fitness(chord: str, notes: Iterable[str]) -> int:
    chord_notes = set(get_chord_notes(chord))
    notes = set(notes)
    return len(chord_notes.intersection(notes))


def note_mismatch_penalty(chord: str, notes: Iterable[str]) -> int:
    chord_notes = set(get_chord_notes(chord))
    notes = set(notes)
    return len(chord_notes.difference(notes))
