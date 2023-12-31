import random
from copy import copy
from .weighted_formula import WeightedCnf

class Configuration:
    """Configuration that supports indexing with evaluated variables (signed integers)."""
    def __init__(self, formula: WeightedCnf):
        self._formula = formula
        self._variable_cnt: int = formula.variable_cnt
        self.variable_evaluation: list[int] = []
        self.counts_of_satisfied_literals: list[int] = []
        self.sat_weights_sum: int = 0

    def set_random(self):
        self.sat_weights_sum = 0
        self.variable_evaluation = [0]
        for i in range(self._variable_cnt):
            is_true = random.choice((True, False))
            evaluation = i + 1
            if is_true:
                self.sat_weights_sum += self._formula.weights[i]
            else:
                evaluation *= -1

            self.variable_evaluation.append(evaluation)

        # Now copy the evaluation reversed to support negative indexes.
        cpy = copy(self.variable_evaluation)
        cpy.reverse()
        self.variable_evaluation.extend(cpy)
        self.variable_evaluation.pop() # Pop the final 0

        for clause, i in self._formula.cnf:
            sat_literal_cnt = 0
            for variable in clause:
                if self.evaluate_variable(variable):
                    sat_literal_cnt += 1

            self.counts_of_satisfied_literals.append(sat_literal_cnt)

    def from_config(self, other: "Configuration"):
        self._formula = other._formula
        self._variable_cnt = other._variable_cnt
        self.variable_evaluation = copy(other.variable_evaluation)
        self.counts_of_satisfied_literals = copy(other.counts_of_satisfied_literals)
        self.sat_weights_sum = other.sat_weights_sum

    def set_variable(self, variable_name: int, value: bool):
        original_value = self.variable_evaluation[variable_name]
        variable_name = abs(variable_name)
        new_val = variable_name
        if not value:
            new_val *= -1

        self.variable_evaluation[variable_name] = new_val
        self.variable_evaluation[-variable_name] = new_val
        if new_val != original_value:
            self._update_sat_counts(variable_name)
            if value:
                self.sat_weights_sum += self._formula.weights[variable_name - 1]
            else:
                self.sat_weights_sum -= self._formula.weights[variable_name - 1]

    def flip_variable(self, variable_name: int):
        was_true = self.variable_evaluation[variable_name] > 0
        self.variable_evaluation[variable_name] *= -1
        self.variable_evaluation[-variable_name] *= -1
        self._update_sat_counts(variable_name)
        if was_true:
            self.sat_weights_sum -= self._formula.weights[variable_name - 1]
        else:
            self.sat_weights_sum += self._formula.weights[variable_name - 1]

    def _update_sat_counts(self, variable_name: int):
        for clause, clause_index in self._formula.clauses_per_var[variable_name]:
            new_sat_cnt = 0
            for variable in clause:
                new_sat_cnt += self.evaluate_variable(variable)

            self.counts_of_satisfied_literals[clause_index] = new_sat_cnt

    def evaluate_variable(self, variable_name: int) -> bool:
        # variable_name is f.e. "2" or "-1" or "-15".
        # So it contains variable name plus evaluation.
        # Checks if the variable evaluation is in current configuration.
        return variable_name == self.variable_evaluation[variable_name]

    def get_evaluation(self) -> str:
        evaluation = self.variable_evaluation[1 : self._variable_cnt + 1]
        return " ".join(str(eval) for eval in evaluation)
