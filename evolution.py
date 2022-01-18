from __future__ import annotations

from dataclasses import dataclass
from operator import itemgetter
from typing import Tuple, List, Callable, TypeVar, Optional

import random

import numpy as np


class Gene:
    def mutate(self, p: float = 1) -> Gene:
        raise NotImplementedError

    def crossover(self, gene: Gene, p: float = 1) -> Tuple[Gene, Gene]:
        raise NotImplementedError


@dataclass(frozen=True)
class HarmonyGene(Gene):
    gene: List[str]
    alphabet: List[str]

    def __len__(self):
        return len(self.gene)

    def __str__(self):
        return f"HarmonyGene({str(self.gene)})"

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self.gene[item]

    def crossover(self, gene: HarmonyGene, p: float = 1) -> Tuple[HarmonyGene, HarmonyGene]:
        # single point crossover
        assert len(self) == len(gene)

        if random.random() >= p:
            return self, gene

        p = random.randint(1, len(self) - 1)

        return (
            HarmonyGene(self.gene[:p] + gene.gene[p:], self.alphabet),
            HarmonyGene(gene.gene[:p] + self.gene[p:], self.alphabet)
        )

    def mutate(self, p: float = 1) -> HarmonyGene:
        # choose a random chord as a mutation
        return HarmonyGene(
            [random.choice(self.alphabet) if random.random() < p else x for x in self.gene],
            self.alphabet
        )


def initialize_population(n_population: int, gene_length: int, alphabet: List[str]) -> List[HarmonyGene]:
    return [HarmonyGene([random.choice(alphabet) for _ in range(gene_length)], alphabet) for _ in range(n_population)]


def tournament(population: List[Gene], scores: List[float], k: int) -> Tuple[Gene, float]:
    return max(random.choices(list(zip(population, scores)), k=k), key=itemgetter(1))


GeneType = TypeVar('GeneType', bound=Gene)


def genetic_algorithm(
        optimize_func: Callable[[GeneType], float],
        initial_population: List[GeneType],
        p_crossover: float,
        p_mutation: float,
        epochs: int,
        p_location_mutation: Optional[float] = None
) -> Tuple[GeneType, float]:
    if p_location_mutation is None:
        p_location_mutation = 1 / len(initial_population[0])

    population = initial_population
    scores = list(map(optimize_func, initial_population))

    best_idx = np.argmax(scores)
    best_solution = population[best_idx]
    best_score = scores[best_idx]

    for i in range(epochs):
        next_population = []
        next_scores = []

        for i in range(0, len(population), 2):
            parent_1, _ = tournament(population, scores, 3)
            parent_2, _ = tournament(population, scores, 3)

            for child in parent_1.crossover(parent_2, p=p_crossover)[:int(i + 2 > len(population)) + 1]:
                if random.random() < p_mutation:
                    child = child.mutate(p=p_location_mutation)
                score = optimize_func(child)

                next_population.append(child)
                next_scores.append(score)

                if score > best_score:
                    best_score = score
                    best_solution = child

        population = next_population
        scores = next_scores

    return best_solution, best_score
