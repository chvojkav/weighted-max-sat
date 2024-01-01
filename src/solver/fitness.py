from typing import Callable
from weighted_formula.weighted_formula import WeightedCnf
from weighted_formula.configuration import Configuration


fitness_strategy_t = Callable[[WeightedCnf, Configuration], float]


def unsatisfied_clause_count(cnf: WeightedCnf, config: Configuration) -> float:
    sat_cnt = 0
    for sat_literal_cnt in config.counts_of_satisfied_literals:
        if sat_literal_cnt != 0:
            sat_cnt += 1

    return len(cnf.cnf) - sat_cnt


def satisfied_clause_count(cnf: WeightedCnf, config: Configuration) -> float:
    sat_cnt = 0
    for sat_literal_cnt in config.counts_of_satisfied_literals:
        if sat_literal_cnt != 0:
            sat_cnt += 1

    return -sat_cnt


def weigted_penalized_satisfied_clause_count(cnf: WeightedCnf, config: Configuration) -> float:
    sat_cnt = 0
    for sat_literal_cnt in config.counts_of_satisfied_literals:
        if sat_literal_cnt != 0:
            sat_cnt += 1

    weighted_fitness = sat_cnt + (config.sat_weights_sum / cnf.weights_sum) * 0.9999

    # The algorithm is minimazing, so we need to return negative value.
    return -weighted_fitness


def weights(cnf: WeightedCnf, config: Configuration) -> float:
    weight_sum = config.sat_weights_sum

    return -weight_sum
