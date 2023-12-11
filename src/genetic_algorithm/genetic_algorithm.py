from random import choices, shuffle
from typing import Callable, Iterable, TextIO
from more_itertools import grouper

from genetic_algorithm.individual import Individual
from genetic_algorithm.population import Population
from .selection import TournamentSelection, selection_t


# To increase initial diversity.
INITIAL_GENERATION_MULTIPLIER = 5


def genetic_algorithm(individual_generator: Callable[[], Individual], 
                      population_size: int,
                      number_of_generations: int,
                      selection: selection_t = TournamentSelection(),
                      crossover_probability: float = 0.9,
                      mutation_rate: float = 0.01,
                      elitism: int = 1,
                      debug_stream: TextIO | None = None) -> Individual:
    """Runs a round of a genetic algorithm.
    
    :param individual_generator: Callable returning (possibly random) Individuals. Used to generate the initial population.
    :param population_size: Size of a population. int > 0
    :param number_of_generations: Number of generations. int >= 0
    :param selection: Selection stategy. Used to select 'n' fittest individuals.
    :param crossover_probability: Probability that individual goes into crossover. 0 <= float <= 1
    :param mutation_rate: Probability of mutation of each individual. 0 <= float <= 1
    :param elitism: How many best individuals are copied from previous generation to the new one. Note that the greater elitism is the fewer new individuals are created. 0 <= int <= population_size
    :param debug_stream: IO stream for debug statistics about population.
    
    :returns: The fittest individual in the last generation.
    """
    assert population_size > 0
    assert number_of_generations >= 0
    assert 0 <= crossover_probability <= 1
    assert 0 <= mutation_rate <= 1
    assert 0 <= elitism <= population_size

    population = Population([individual_generator() for _ in range(population_size * INITIAL_GENERATION_MULTIPLIER)])

    try:
        for i in range(number_of_generations):
            elites = list(population.get_elites(how_many=elitism))
            selected = list(selection(population, population_size - elitism))
            
            if debug_stream is not None:
                dp = Population(elites + selected)
                debug_stream.write(f"{i},{dp.fittest},{dp.mean},{dp.median},{dp.least_fit}\n")

            newborns = []
            if crossover_probability > 0:
                newborns = _breed(elites + selected, crossover_probability)
            
            mutable_individuals = selected + newborns  # Don't mutate elites.
            if mutation_rate > 0:
                mutable_individuals = _mutate(mutable_individuals, mutation_rate)
            
            population = Population(elites + mutable_individuals)
    except KeyboardInterrupt:
        pass

    return next(iter(population.get_elites(1)))


def _breed(fertile_population: list[Individual],
           crossover_probability: float) -> list[Individual]:
    # Random permutation so that it's random who breeds with whom.
    shuffle(fertile_population)

    to_breed: list[Individual] = []
    for individual in fertile_population:
        if choices([True, False], cum_weights=[crossover_probability, 1]):
            to_breed.append(individual)
    
    couples = list(grouper(to_breed, 2))

    offspring = []
    for A, B in couples:
        if A is not None and B is not None:
            offspring.extend(A.breed(B))

    return offspring


def _mutate(mutable_population: Iterable[Individual],
            mutation_rate: float) -> list[Individual]:
    new_population = []
    for individual in mutable_population:
        if choices([True, False], cum_weights=[mutation_rate, 1]):
            new_population.append(individual.mutate())
        else:
            new_population.append(individual)

    return new_population
