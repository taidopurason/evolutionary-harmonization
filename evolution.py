from __future__ import annotations

from dataclasses import dataclass
from operator import itemgetter
from typing import Tuple, List, Callable, TypeVar, Optional

import random

import numpy as np


class Gene:
    def mutate(self, p: float = 1) -> Gene:
        raise NotImplementedError

    def crossover(self, gene: Gene) -> Tuple[Gene, Gene]:
        raise NotImplementedError


class Selection:
    def select(self, population: List[Gene], scores: List[float]) -> Tuple[Gene, float]:
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

    @staticmethod
    def initialize_population(n_population: int, gene_length: int, alphabet: List[str]) -> List[HarmonyGene]:
        return [
            HarmonyGene([random.choice(alphabet) for _ in range(gene_length)], alphabet) for _ in range(n_population)
        ]

    def crossover(self, gene: HarmonyGene) -> Tuple[HarmonyGene, HarmonyGene]:
        # single point crossover
        assert len(self) == len(gene)

        p = random.randint(1, len(self) - 1)

        return (
            HarmonyGene(self.gene[:p] + gene.gene[p:], self.alphabet),
            HarmonyGene(gene.gene[:p] + self.gene[p:], self.alphabet)
        )

    def mutate(self, p: float = 1) -> HarmonyGene:
        return HarmonyGene(
            [random.choice(self.alphabet) if random.random() < p else x for x in self.gene],
            self.alphabet
        )


class Callback:
    def on_begin(self):
        pass

    def on_end(self):
        pass

    def on_epoch_end(self, best_solution: Gene, best_score: float, epoch: int) -> bool:
        return False


class EarlyStopping(Callback):
    def __init__(self, patience):
        self.patience = patience
        self.best_score = None
        self.not_improved = 0

    def on_begin(self):
        self.not_improved = 0

    def on_epoch_end(self, best_solution: Gene, best_score: float, epoch: int) -> bool:
        if self.best_score is None:
            self.best_score = best_score

        if best_score <= self.best_score:
            self.not_improved += 1
            if self.not_improved >= self.patience:
                logger.info(f"The fitness has not improved for {self.patience} epochs. Stopping training at epoch {epoch}")
                return True
        else:
            self.not_improved = 0
            self.best_score = best_score


@dataclass
class TournamentSelection(Selection):
    k: int

    def select(self, population: List[Gene], scores: List[float]) -> Tuple[Gene, float]:
        return max(random.choices(list(zip(population, scores)), k=self.k), key=itemgetter(1))


GeneType = TypeVar('GeneType', bound=Gene)


def genetic_algorithm(
        optimize_func: Callable[[GeneType], float],
        initial_population: List[GeneType],
        selection: Selection,
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

    for j in range(epochs):
        next_population = []
        next_scores = []

        for i in range(0, len(population), 2):
            parent_1, score_1 = selection.select(population, scores)
            parent_2, score_2 = selection.select(population, scores)

            if random.random() < p_crossover:
                children = parent_1.crossover(parent_2)
                child_scores = (None, None)
            else:
                children = (parent_1, parent_2)
                child_scores = (score_1, score_2)

            for child, score in list(zip(children, child_scores))[:int(i + 1 < len(population)) + 1]:
                if random.random() < p_mutation:
                    child = child.mutate(p=p_location_mutation)
                    score = None

                if score is None:
                    score = optimize_func(child)

                next_population.append(child)
                next_scores.append(score)

                if score > best_score:
                    best_score = score
                    best_solution = child

        population = next_population
        scores = next_scores

    return best_solution, best_score
