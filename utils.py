from typing import Iterable, List

from mingus.containers import Note
from mingus.core.chords import from_shorthand


def get_chord_notes(chord: str) -> List[str]:
    return from_shorthand(chord)


def note_match_fitness(chord: str, notes: Iterable[str]) -> float:
    chord_notes = set(get_chord_notes(chord))
    notes = set(map(lambda x: Note(x).name, notes))
    return len(chord_notes.intersection(notes)) / len(chord_notes)


def note_mismatch_penalty(chord: str, notes: Iterable[str]) -> float:
    chord_notes = set(get_chord_notes(chord))
    notes = set(map(lambda x: Note(x).name, notes))
    return len(chord_notes.difference(notes)) / len(chord_notes)
