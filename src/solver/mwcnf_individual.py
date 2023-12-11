from copy import copy
from genetic_algorithm.individual import Individual
from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf

from .fitness import fitness_strategy_t
from .crossover import crossover_strategy_t
from .mutation import mutation_strategy_t


class MwcnfIndividual(Individual):
    def __init__(self,
                 formula: WeightedCnf,
                 config: Configuration,
                 fitness_getter: fitness_strategy_t,
                 breeder: crossover_strategy_t,
                 mutator: mutation_strategy_t) -> None:
        super().__init__()
        self.formula = formula
        self.config = config
        self.fitness_getter = fitness_getter
        self.breeder = breeder
        self.mutator = mutator
    
    def fitness(self) -> float:
        """Posifive number. The less, the better."""
        return self.fitness_getter(self.formula, self.config)
    
    def mutate(self) -> "Individual":
        mutant = copy(self)
        mutant.config = self.mutator(self.formula, self.config)
        return mutant
    
    def breed(self, other: "Individual") -> tuple["Individual", "Individual"]:
        if not isinstance(other, MwcnfIndividual):
            raise TypeError

        new_configs = self.breeder(self.formula, self.config, other.config)
        offspring = (copy(self), copy(other))
        offspring[0].config = new_configs[0]
        offspring[1].config = new_configs[1]
        
        return offspring
