from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf

from .crossover import uniform_crossover
from .fitness import unsatisfied_clause_count
from .mutation import flip_random_variable
from .mwcnf_individual import MwcnfIndividual


class MwcnfGenerator:
    def __init__(self, formula: WeightedCnf):
        self.formula = formula

    def __call__(self) -> MwcnfIndividual:
        config = Configuration(self.formula.clause_cnt)
        config.set_random()

        return MwcnfIndividual(self.formula,
                               config,
                               fitness_getter=unsatisfied_clause_count,
                               breeder=uniform_crossover,
                               mutator=flip_random_variable)
