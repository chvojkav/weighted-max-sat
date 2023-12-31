from math import log, sqrt
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

    weight_sum = 0
    for i, weight in enumerate(cnf.weights, start=1):
        if config.evaluate_variable(i):
            weight_sum += weight

    teoretical_max_weight = cnf.weights_sum

    adjusted_weight = weight_sum / teoretical_max_weight

    # This ensures that even all weights together are less important than one satisfied clause
    adjusted_weight *= 0.9999999
    assert 0 <= adjusted_weight < 1

    weighted_fitness = sat_cnt + adjusted_weight

    penalized_fitness = weighted_fitness

    # The algorithm is minimazing, so we need to return negative value.
    return -penalized_fitness


def weights(cnf: WeightedCnf, config: Configuration) -> float:
    weight_sum = 0
    for i, weight in enumerate(cnf.weights, start=1):
        if config.evaluate_variable(i):
            weight_sum += weight

    return -weight_sum
