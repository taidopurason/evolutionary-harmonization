from typing import Iterable, List

from mingus.containers import Note
from mingus.core.chords import from_shorthand
from mingus.core.progressions import determine

good_progressions = [['I', 'IV', 'V', 'I', 'I'],
                     ['I', 'IV', 'vi', 'V', 'I'],
                     ['I', 'IV', 'I', 'V', 'I'],
                     ['I', 'V', 'IV', 'V', 'I'],
                     ['I', 'vi', 'IV', 'V', 'I'],
                     ['I', 'V', 'vi', 'IV', 'I']]

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

def chord_progression_fitness(chords: List[str], key: str) -> float:
    progression = []
    for chord in chords:
        determined_chord = determine(get_chord_notes(chord), key, True)[0]
        progression.append(determined_chord)

    if progression in good_progressions:
        return 0.5
    elif progression[-2:] in [['V', 'I'], ['IV', 'I']]:
        return 0.25
    elif progression[-1] == 'I':
        return 0.1
    else:
        return -0.5
