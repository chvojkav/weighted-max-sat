from copy import deepcopy
from random import random
from typing import Callable

from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf


mutation_strategy_t = Callable[[WeightedCnf, Configuration], Configuration]


def flip_random_variable(unused: WeightedCnf,
                         config: Configuration) -> Configuration:
    _ = unused

    mutant = deepcopy(config)
    bit_mutation_threshold = 1 / config._variable_cnt
    for var in range(1, config._variable_cnt + 1):
        if random() < bit_mutation_threshold:
            mutant.flip_variable(var)

    return mutant
