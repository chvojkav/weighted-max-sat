from typing import Callable
from ..weighted_formula.weighted_formula import WeightedCnf
from ..weighted_formula.configuration import Configuration

# An abstract metric of a formula.
# formula_metric_t = Callable[[WeightedCnf], float]

# An abstract metric of a configuration.
configuration_metric_t = Callable[[WeightedCnf, Configuration], float]

def unsatisfied_clause_count(cnf: WeightedCnf, config: Configuration) -> float:
    sat_cnt = 0
    for clause in cnf.cnf:
        for variable in clause[0]:
            if config.evaluate_variable(variable):
                # One literal of clause is satisfied hence whole clause is satisfied.
                sat_cnt += 1
                break
    
    return len(cnf.cnf) - sat_cnt
