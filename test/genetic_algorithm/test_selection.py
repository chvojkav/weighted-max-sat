from genetic_algorithm.individual import Individual
from genetic_algorithm.population import Population
from genetic_algorithm.selection import TournamentSelection


class IndividualStub(Individual):
    def __init__(self, fitness):
        self._fitness = fitness
    
    def fitness(self) -> float:
        return self._fitness


def test_resulting_population_size_correct():
    selector = TournamentSelection()
    population = Population([IndividualStub(1), IndividualStub(2), IndividualStub(3)])
    sizes_to_test = [1, 10, 20, 100, 1000]
    for size in sizes_to_test:
        resulting_population = selector(population, size)
        assert len(resulting_population) == size


def test_selects_elite_if_population_size_eq_tournament_size():
    selector = TournamentSelection(3)
    population = Population([IndividualStub(1), IndividualStub(2), IndividualStub(3)])
    resulting_population = selector(population, 3)
    for individual in resulting_population:
        assert individual.fitness() == 1


def test_least_fit_not_selected_with_tournament_size_eq_2():
    selector = TournamentSelection(2)
    population = Population([IndividualStub(1), IndividualStub(2), IndividualStub(3)])
    resulting_population = selector(population, 100)
    for individual in resulting_population:
        assert individual.fitness() != 3
