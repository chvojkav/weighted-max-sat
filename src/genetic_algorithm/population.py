from random import sample
from typing import Iterable

from .individual import Individual

class Population:
    def __init__(self,
                 individuals: Iterable[Individual],
                 expected_elitism: int = 0):
        self.individuals = list(individuals)
        self.expected_elitism = expected_elitism
        if expected_elitism in (0, 1):
            # As sorting is done mainly to enable getting arbitrary number of elites,
            # if we know that we'll need at most one elite, we don't need to sort.
            self._fittest = min(self.individuals)
        else:
            self.individuals.sort()
            self._fittest = self.individuals[0]
    
    @property
    def size(self) -> int:
        return len(self.individuals)
    
    def random_sample(self, sample_size: int = 1) -> Iterable[Individual]:
        return sample(self.individuals, sample_size)

    def get_elites(self, how_many: int = 1) -> Iterable[Individual]:
        if how_many == 1:
            return [self._fittest]
        elif how_many == 0:
            return []

        if self.expected_elitism <= 1:
            # We did not expect to need individuals sorted, but we do...
            self.individuals.sort()

        return self.individuals[:how_many]
