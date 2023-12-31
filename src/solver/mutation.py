from random import random
from typing import Callable

from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf


mutation_strategy_t = Callable[[WeightedCnf, Configuration, float], Configuration]


def flip_random_variable(unused: WeightedCnf,
                         config: Configuration,
                         mutation_probability: float) -> Configuration:
    _ = unused

    mutant = None
    for var in range(1, config._variable_cnt + 1):
        if random() < mutation_probability:
            if mutant is None:
                mutant = Configuration(0)
                mutant.from_config(config)
            mutant.flip_variable(var)

    if mutant is None:
        mutant = Configuration(0)
        mutant.from_config(config)

    return mutant
