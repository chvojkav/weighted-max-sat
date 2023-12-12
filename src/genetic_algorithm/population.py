from random import sample
from typing import Iterable
from numpy import mean, median

from .individual import Individual

class Population:
    def __init__(self,
                 individuals: Iterable[Individual],
                 expected_elitism: int):
        self.individuals = list(individuals)
        self.expected_elitism = expected_elitism
        if expected_elitism <= 1:
            # As sorting is done mainly to enable getting arbitrary number of elites,
            # if we know that we'll need at most one elite, we don't need to sort.
            self.individuals.sort()
            self._fittest = self.individuals[0]
            self._least_fit = self.individuals[-1]
        else:
            self._fittest = min(self.individuals)
            self._least_fit = max(self.individuals)

        fitnesses = [individual.fitness() for individual in self.individuals]
        self.mean = mean(fitnesses)
        self.median = median(fitnesses)
    
    @property
    def size(self) -> int:
        return len(self.individuals)
    
    @property
    def fittest(self) -> float:
        return self._fittest.fitness()
    
    @property
    def least_fit(self) -> float:
        return self._least_fit.fitness()
    
    def random_sample(self, sample_size: int = 1) -> Iterable[Individual]:
        return sample(self.individuals, sample_size)

    def get_elites(self, how_many: int = 1) -> Iterable[Individual]:
        if how_many == 1:
            return [self._fittest]

        if how_many != 0 and self.expected_elitism > 1:
            # We did not expect to need individuals sorted, but we do...
            self.individuals.sort()

        return self.individuals[:how_many]
