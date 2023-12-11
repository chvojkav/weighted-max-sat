from typing import Callable

from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf


mutation_strategy_t = Callable[[WeightedCnf, Configuration], Configuration]
