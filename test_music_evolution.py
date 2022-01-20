from fractions import Fraction
from typing import Iterable, Tuple

from mingus.midi.midi_file_out import write_Composition

from evolution import HarmonyGene, genetic_algorithm, TournamentSelection, EarlyStopping
from mingus_utils import create_composition, test_melody, test_chords
from utils import note_match_fitness, note_mismatch_penalty, chord_progression_fitness


def fitness(gene: HarmonyGene, melody: Iterable[Tuple[Tuple[str, Fraction]]], key: str) -> float:
    melody_notes = set(note[0] for bar in melody for note in bar)

    fitness = 0
    for chord, bar in zip(gene, melody):
        bar_notes = set(note[0] for note in bar)
        fitness += note_match_fitness(chord, bar_notes)
        fitness -= 0.7 * note_mismatch_penalty(chord, bar_notes)
        fitness -= 0.3 * note_mismatch_penalty(chord, melody_notes)

    fitness += chord_progression_fitness(gene.gene, key)

    return fitness


if __name__ == "__main__":
    # alphabet = get_notes("F")
    # alphabet = ['Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#']
    # alphabet += [a + "m" for a in alphabet]

    # only diatonic chords
    alphabet = ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"]

    key = "F"
    n_population = len(test_chords)

    print("Alphabet", alphabet)
    initial_pop = HarmonyGene.initialize_population(n_population * 10, n_population, alphabet)
    generated_chords, score = genetic_algorithm(
        lambda x: fitness(x, test_melody, key),
        initial_pop,
        TournamentSelection(5),
        p_crossover=0.8,
        p_mutation=0.3,
        epochs=500,
        callbacks=[EarlyStopping(30)]
    )
    print("Best score:", score)
    print("Generated chords", generated_chords)

    write_Composition("generated.midi", create_composition(test_melody, generated_chords))
    write_Composition("correct.midi", create_composition(test_melody, test_chords))
