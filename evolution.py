from __future__ import annotations

from typing import Tuple, List, Set, Iterable

import random


class Gene:
    def mutate(self, p: float) -> Gene:
        raise NotImplementedError

    def crossover(self, gene: Gene, p: float) -> Gene:
        raise NotImplementedError


class HarmonyGene(Gene):
    def __init__(self, chords: List[str], alphabet: List[str]):
        self.gene = chords
        self.alphabet = alphabet

    def __len__(self):
        return len(self.gene)

    def __str__(self):
        return f"HarmonyGene({str(self.gene)})"

    def __repr__(self):
        return str(self)

    def crossover(self, gene: HarmonyGene, p: float) -> Tuple[HarmonyGene, HarmonyGene]:
        # single point crossover
        assert len(self) == len(gene)

        if random.random() >= p:
            return self, gene

        p = random.randint(1, len(self) - 1)

        return (
            HarmonyGene(self.gene[:p] + gene.gene[p:], self.alphabet),
            HarmonyGene(gene.gene[:p] + self.gene[p:], self.alphabet)
        )

    def mutate(self, p: float) -> HarmonyGene:
        # choose a random chord as a mutation
        return HarmonyGene(
            [random.choice(self.alphabet) if random.random() < p else x for x in self.gene],
            self.alphabet
        )


def initialize_population(n_population: int, n_chords: int, chords: List[str]) -> List[HarmonyGene]:
    return [HarmonyGene([random.choice(chords) for _ in range(n_chords)], chords) for _ in range(n_population)]


def genetic_algorithm(initial_population: List[Gene], p_crossover, p_mutation):
    pass
