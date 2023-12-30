from math import log, sqrt
from typing import Callable
from weighted_formula.weighted_formula import WeightedCnf
from weighted_formula.configuration import Configuration


fitness_strategy_t = Callable[[WeightedCnf, Configuration], float]


def unsatisfied_clause_count(cnf: WeightedCnf, config: Configuration) -> float:
    sat_cnt = 0
    for clause in cnf.cnf:
        for variable in clause[0]:
            if config.evaluate_variable(variable):
                # One literal of clause is satisfied hence whole clause is satisfied.
                sat_cnt += 1
                break
    
    return len(cnf.cnf) - sat_cnt


def satisfied_clause_count(cnf: WeightedCnf, config: Configuration) -> float:
    sat_cnt = 0
    for clause in cnf.cnf:
        for variable in clause[0]:
            if config.evaluate_variable(variable):
                # One literal of clause is satisfied hence whole clause is satisfied.
                sat_cnt += 1
                break
    
    return -sat_cnt


def weigted_penalized_satisfied_clause_count(cnf: WeightedCnf, config: Configuration) -> float:
    sat_cnt = 0
    for clause in cnf.cnf:
        for variable in clause[0]:
            if config.evaluate_variable(variable):
                # One literal of clause is satisfied hence whole clause is satisfied.
                sat_cnt += 1
                break
    
    weight_sum = 0
    for i, weight in enumerate(cnf.weights, start=1):
        if config.evaluate_variable(i):
            weight_sum += weight

    teoretical_max_weight = cnf.weights_sum

    adjusted_weight = weight_sum / teoretical_max_weight

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
