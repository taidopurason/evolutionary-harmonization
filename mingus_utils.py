from typing import Tuple, Iterable

from mingus.containers import Bar, Track, NoteContainer, Composition
from mingus.midi.midi_file_out import write_Composition

from fractions import Fraction


def dot(x: Fraction) -> Fraction:
    return x + x / 2


def to_mingus(x: Fraction) -> float:
    return float(1 / x)


whole = Fraction(1)
half = Fraction(1, 2)
quarter = Fraction(1, 4)
eighth = Fraction(1, 8)
sixteenth = Fraction(1, 16)

# lithne näide

# eeltakt + 4 takti sünnipäeva laulu
test_melody = (
    (
        ("C-5", dot(eighth)),
        ("C-5", sixteenth)
    ),
    (
        ("D-5", quarter),
        ("C-5", quarter),
        ("F-5", quarter)
    ),
    (
        ("E-5", half),
        ("C-5", dot(eighth)),
        ("C-5", sixteenth)
    ),
    (
        ("D-5", quarter),
        ("C-5", quarter),
        ("G-5", quarter)
    ),
    (
        ("F-5", half),
    )
)

# akordid iga takti algusesse
test_chords = (
    "",
    "F",
    "C",
    "C",
    "F"
)

def create_melody(melody: Iterable[Tuple[Tuple[str, Fraction]]]) -> Track:
    melody_track = Track()
    for bar in melody:
        bar_length = sum(note[1] for note in bar)
        ratio = (bar_length.numerator, bar_length.denominator)

        note_bar = Bar(meter=ratio)

        for note, duration in bar:
            if not note_bar.place_notes(note, to_mingus(duration)):
                raise ValueError("more notes than fit in a bar")


        melody_track.add_bar(note_bar)

    return melody_track


def create_composition(melody: Iterable[Tuple[Tuple[str, Fraction]]], chords: Iterable[str]) -> Composition:
    # midi genereerimine
    melody_track = Track()
    chord_track = Track()

    for chord, bar in zip(chords, melody):
        # võtab nootide järgi taktimõõdu
        bar_length = sum(note[1] for note in bar)
        ratio = (bar_length.numerator, bar_length.denominator)

        note_bar = Bar(meter=ratio)
        chord_bar = Bar(meter=ratio)

        # lisab noodid
        for note, duration in bar:
            if not note_bar.place_notes(note, to_mingus(duration)):
                raise ValueError("more notes than fit in a bar")

        if not chord_bar.place_notes(NoteContainer().from_chord_shorthand(chord) if chord else None,
                                     to_mingus(bar_length)):
            raise ValueError("more notes than fit in a bar")

        melody_track.add_bar(note_bar)
        chord_track.add_bar(chord_bar)

    composition = Composition()
    composition.add_track(melody_track)
    composition.add_track(chord_track)

    return composition

if __name__ == "__main__":
    write_Composition("test.midi", create_composition(test_melody, test_chords))
