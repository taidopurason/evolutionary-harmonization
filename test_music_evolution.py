from fractions import Fraction
from typing import Iterable, Tuple

from evolution import HarmonyGene, genetic_algorithm, TournamentSelection
from mingus_test import write_composition, test_melody, test_chords
from utils import get_chord_notes, note_match_fitness, note_mismatch_penalty


def fitness(gene: HarmonyGene, melody: Iterable[Tuple[Tuple[str, Fraction]]]) -> float:
    fitness = 0
    for chord, bar in zip(gene, melody):
        bar_notes = set(b[0] for b in bar)
        fitness += note_match_fitness(chord, bar_notes) - 0.5*note_mismatch_penalty(chord, bar_notes)

    return fitness


if __name__ == "__main__":
    write_composition(test_melody, test_chords, "correct.midi")

    alphabet = ["C", "D", "E", "F", "G", "A", "B"]
    alphabet += [a + "m" for a in alphabet]
    n_population = len(test_chords)

    initial_pop = HarmonyGene.initialize_population(n_population * 10, n_population, alphabet)
    generated_chords, score = genetic_algorithm(
        lambda x: fitness(x, test_melody),
        initial_pop,
        TournamentSelection(5),
        p_crossover=0.8,
        p_mutation=0.3,
        epochs=700
    )
    print("Best score:", score)
    print("Generated chords", generated_chords)
    write_composition(test_melody, generated_chords, "generated.midi")
