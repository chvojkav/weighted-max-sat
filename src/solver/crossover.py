from random import choice
from typing import Callable
from weighted_formula.configuration import Configuration

from weighted_formula.weighted_formula import WeightedCnf


crossover_strategy_t = Callable[[WeightedCnf, Configuration, Configuration],
                                tuple[Configuration, Configuration]]


def uniform_crossover(formula: WeightedCnf,
                      a: Configuration,
                      b: Configuration) -> tuple[Configuration, Configuration]:
    offspring_a = Configuration(formula)
    offspring_a.from_config(a)
    offspring_b = Configuration(formula)
    offspring_b.from_config(b)

    for variable in range(1, a._variable_cnt + 1):
        if choice([True, False]):
            offspring_a.set_variable(variable, b.evaluate_variable(variable))
            offspring_b.set_variable(variable, a.evaluate_variable(variable))

    return offspring_a, offspring_b
