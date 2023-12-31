from math import ceil
from random import random, shuffle
from typing import Callable, Iterable, TextIO
from more_itertools import grouper
from numpy import mean, median

from genetic_algorithm.individual import Individual
from genetic_algorithm.population import Population
from .selection import TournamentSelection, selection_t


def genetic_algorithm(individual_generator: Callable[[], Individual], 
                      population_size: int,
                      number_of_generations: int,
                      selection: selection_t = TournamentSelection(),
                      crossover_probability: float = 0.9,
                      mutation_rate: float = 0.01,
                      elitism: int = 1,
                      terminate_on_stagnation_in_x_generations: int | float | None = None,
                      debug_stream: TextIO | None = None) -> tuple[Individual, int]:
    """Runs a round of a genetic algorithm.
    
    :param individual_generator: Callable returning (possibly random) Individuals. Used to generate the initial population.
    :param population_size: Size of a population. int > 0
    :param number_of_generations: Number of generations. int >= 0
    :param selection: Selection stategy. Used to select 'n' fittest individuals.
    :param crossover_probability: Probability that individual goes into crossover. 0 <= float <= 1
    :param mutation_rate: Probability of mutation of each individual. 0 <= float <= 1
    :param elitism: How many best individuals are copied from previous generation to the new one. Note that the greater elitism is the fewer new individuals are created. 0 <= int <= population_size
    :param terminate_on_stagnation_in_x_generations: For how many generations the population should stagnate to terminate. Can also be a float from interval (0, 1), in which case it is a part of number of generations.
    :param debug_stream: IO stream for debug statistics about population.
    
    :returns: The fittest individual in the last generation, and the number of generations.
    """
    assert population_size > 0
    assert number_of_generations >= 0
    assert 0 <= crossover_probability <= 1
    assert 0 <= mutation_rate <= 1
    assert 0 <= elitism <= population_size
    if isinstance(terminate_on_stagnation_in_x_generations, float):
        assert 0 < terminate_on_stagnation_in_x_generations < 1
        terminate_on_stagnation_in_x_generations = ceil(number_of_generations * terminate_on_stagnation_in_x_generations)

    if isinstance(terminate_on_stagnation_in_x_generations, int):
        assert 0 < terminate_on_stagnation_in_x_generations <= number_of_generations

    i = 0
    population = Population([individual_generator() for _ in range(population_size)],
                            expected_elitism=elitism)

    # Serves for termination on stagnation.
    best = next(iter(population.get_elites()))
    last_improvement = i

    try:
        for i in range(number_of_generations):
            elites = list(population.get_elites(how_many=elitism))
            selected = list(selection(population, population_size - elitism))
            
            if debug_stream is not None:
                fits = [individual.fitness() for individual in elites + selected]
                debug_stream.write(f"{i},{min(fits)},{mean(fits)},{median(fits)},{max(fits)}\n")

            if terminate_on_stagnation_in_x_generations is not None:
                current_best = next(iter(population.get_elites()))
                if current_best < best:
                    best = current_best
                    last_improvement = i

                if i - last_improvement > terminate_on_stagnation_in_x_generations:
                    break

            newborns = []
            if crossover_probability > 0:
                newborns = _breed(elites + selected, crossover_probability)
            
            mutants = []
            if mutation_rate > 0:
                mutants = _mutate(selected + newborns + elites, mutation_rate)
            
            population = Population(elites + selected + newborns + mutants,
                                    expected_elitism=elitism)
    except KeyboardInterrupt:
        pass

    return next(iter(population.get_elites(1))), i


def _breed(fertile_population: list[Individual],
           crossover_probability: float) -> list[Individual]:
    # Random permutation so that it's random who breeds with whom.
    shuffle(fertile_population)

    to_breed: list[Individual] = []
    for individual in fertile_population:
        if random() < crossover_probability:
            to_breed.append(individual)
    
    couples = list(grouper(to_breed, 2))

    offspring = []
    for A, B in couples:
        if A is not None and B is not None:
            offspring.extend(A.breed(B))

    return offspring


def _mutate(population: Iterable[Individual],
            mutation_rate: float) -> list[Individual]:
    mutants = []
    for individual in population:
        mutants.append(individual.mutate(mutation_rate))

    return mutants
