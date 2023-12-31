from typing import Iterable


clause3_t = tuple[int, int, int]
indexed_clause3_t = tuple[clause3_t, int]
cnf_t = tuple[indexed_clause3_t, ...]
weights_t = tuple[int, ...]


class WeightedCnf:
    def __init__(self, cnf: Iterable[clause3_t], weights: weights_t):
        self.weights: weights_t = weights
        self.weights_sum = sum(weights)
        self.cnf: cnf_t = tuple()
        i = -1
        for i, clause in enumerate(cnf):
            self.cnf += ((clause, i),)

        self.clause_cnt = i + 1
        self.variable_cnt = len(weights)
        self.clauses_per_var: dict[int, Iterable[indexed_clause3_t]] = {}

        for i in range(1, self.variable_cnt + 1):
            tmp = self._find_clauses_for_var(cnf, i)
            self.clauses_per_var[i] = tmp
            self.clauses_per_var[-i] = tmp

    @staticmethod
    def _find_clauses_for_var(cnf: Iterable[clause3_t], variable_no: int) -> tuple[indexed_clause3_t, ...]:
        clauses: tuple[indexed_clause3_t, ...] = tuple()
        for i, clause in enumerate(cnf):
            for variable in clause:
                if variable_no == abs(variable):
                    clauses += ((clause, i),)
                    break

        return clauses
