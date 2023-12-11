from random import sample
from typing import Iterable
from numpy import mean, median

from .individual import Individual

class Population:
    def __init__(self, individuals: Iterable[Individual]):
        self.individuals = list(individuals)
        self.individuals.sort()

        fitnesses = [individual.fitness() for individual in self.individuals]
        self.mean = mean(fitnesses)
        self.median = median(fitnesses)
    
    @property
    def size(self) -> int:
        return len(self.individuals)
    
    @property
    def fittest(self) -> float:
        return self.individuals[0].fitness()
    
    @property
    def least_fit(self) -> float:
        return self.individuals[-1].fitness()
    
    def random_sample(self, sample_size: int = 1) -> Iterable[Individual]:
        return sample(self.individuals, sample_size)

    def get_elites(self, how_many: int = 1) -> list[Individual]:
        return self.individuals[:how_many]
