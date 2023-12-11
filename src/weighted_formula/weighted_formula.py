from typing import Iterable


clause3_t = tuple[int, int, int]
indexed_clause3_t = tuple[clause3_t, int]
cnf_t = tuple[indexed_clause3_t, ...]
weights_t = tuple[int, ...]


class WeightedCnf:
    def __init__(self, cnf: Iterable[clause3_t], weights: weights_t):
        self.weights: weights_t = weights
        self.cnf: cnf_t = tuple()
        i = -1
        for i, clause in enumerate(cnf):
            self.cnf += ((clause, i),)
        
        self.clause_cnt = i + 1
