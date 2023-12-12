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
        self._fitness = None
        self.breeder = breeder
        self.mutator = mutator
    
    def fitness(self) -> float:
        """Posifive number. The less, the better."""
        if self._fitness == None:
            self._fitness = self.fitness_getter(self.formula, self.config)
        
        return self._fitness 
    
    def mutate(self) -> "Individual":
        return self.copy(new_config=self.mutator(self.formula, self.config))
    
    def breed(self, other: "Individual") -> tuple["Individual", "Individual"]:
        if not isinstance(other, MwcnfIndividual):
            raise TypeError

        new_configs = self.breeder(self.formula, self.config, other.config)
        return self.copy(new_configs[0]), other.copy(new_configs[1])
    
    def copy(self, new_config: Configuration) -> "Individual":
        ret = copy(self)
        ret.config = new_config
        ret._fitness = None
        return ret
    
    def __repr__(self) -> str:
        return f"MI(fit={self.fitness():.3f})"
