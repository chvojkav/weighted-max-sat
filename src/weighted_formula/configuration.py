import random
from copy import copy
from .weighted_formula import WeightedCnf

class Configuration:
    """Configuration that supports indexing with evaluated variables (signed integers)."""
    def __init__(self, formula: WeightedCnf):
        self._formula = formula
        self._variable_cnt: int = formula.variable_cnt
        self.variable_evaluation: list[int] = []
    
    def set_random(self):
        self.variable_evaluation = [0]
        for i in range(self._variable_cnt):
            is_true = random.choice((True, False))
            evaluation = i + 1
            if not is_true:
                evaluation *= -1

            self.variable_evaluation.append(evaluation)
        
        # Now copy the evaluation reversed to support negative indexes.
        cpy = copy(self.variable_evaluation)
        cpy.reverse()
        self.variable_evaluation.extend(cpy)
        self.variable_evaluation.pop() # Pop the final 0
    
    def from_config(self, other: "Configuration"):
        self._formula = other._formula
        self._variable_cnt = other._variable_cnt
        self.variable_evaluation = copy(other.variable_evaluation)

    def set_variable(self, variable_name: int, value: bool):
        new_val = abs(variable_name)
        if not value:
            new_val *= -1
        
        self.variable_evaluation[variable_name] = new_val
        self.variable_evaluation[-variable_name] = new_val

    def flip_variable(self, variable_name: int):
        self.variable_evaluation[variable_name] *= -1
        self.variable_evaluation[-variable_name] *= -1

    def evaluate_variable(self, variable_name: int) -> bool:
        # variable_name is f.e. "2" or "-1" or "-15".
        # So it contains variable name plus evaluation.
        # Checks if the variable evaluation is in current configuration.
        return variable_name == self.variable_evaluation[variable_name]
    
    def get_evaluation(self) -> str:
        evaluation = self.variable_evaluation[1 : self._variable_cnt + 1]
        return " ".join(str(eval) for eval in evaluation)
