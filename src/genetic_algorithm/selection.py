from typing import Callable, Iterable
from numpy import floor
from numpy.random import choice

from .individual import Individual
from .population import Population

selection_t = Callable[[Population, int], Iterable[Individual]]

class TournamentSelection:
    def __init__(self, tournament_size: float = 1.75):
        """Tournament selection strategy.

        :param tournament_size: Defines how many individuals compete in a single tournament. If number isn't integer, sizes of tournaments vary based on a decimal part.
        """
        assert tournament_size >= 1
        self.tournament_size = tournament_size
        self.base_round_size = int(self.tournament_size)
        self.plus_one_prob = self.tournament_size - self.base_round_size
        self.plus_zero_prob = 1 - self.plus_one_prob
    
    def __call__(self, population: Population, target_size: int) -> list[Individual]:
        assert target_size >=0

        selected_population = []
        for _ in range(target_size):
            round_size = self.base_round_size + \
                            choice([0, 1], 1, p=[self.plus_zero_prob, self.plus_one_prob])[0]
            tournament_participants = population.random_sample(round_size)
            best = min(tournament_participants)
            selected_population.append(best)
        
        return selected_population
