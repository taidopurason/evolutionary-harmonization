from fractions import Fraction
from typing import Iterable, Tuple

from evolution import HarmonyGene, genetic_algorithm, TournamentSelection
from mingus_test import write_composition, test_melody, test_chords
from mingus.core.scales import get_notes
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
    write_composition(test_melody, test_chords, "correct.midi")

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
        epochs=5000
    )
    print("Best score:", score)
    print("Generated chords", generated_chords)
    write_composition(test_melody, generated_chords, "generated.midi")
