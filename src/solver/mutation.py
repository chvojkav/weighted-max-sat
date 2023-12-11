from copy import deepcopy
from random import randrange
from typing import Callable

from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf


mutation_strategy_t = Callable[[WeightedCnf, Configuration], Configuration]


def flip_random_variable(unused: WeightedCnf,
                         config: Configuration) -> Configuration:
    _ = unused

    random_variable = randrange(config._variable_cnt)
    mutant = deepcopy(config)
    mutant.flip_variable(random_variable)

    return mutant
