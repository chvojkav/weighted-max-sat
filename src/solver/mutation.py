from random import random
from typing import Callable

from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf


mutation_strategy_t = Callable[[WeightedCnf, Configuration, float], Configuration]


def flip_random_variable(formula: WeightedCnf,
                         config: Configuration,
                         mutation_probability: float) -> Configuration:
    mutant = Configuration(formula)
    mutant.from_config(config)

    for var in range(1, config._variable_cnt + 1):
        if random() < mutation_probability:
            mutant.flip_variable(var)

    return mutant
