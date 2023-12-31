
from weighted_formula.configuration import Configuration

class FormulaStub:
    def __init__(self):
        self.weights_sum = 0
        self.cnf = None
        self.clause_cnt = 2
        self.variable_cnt = 2


def test_from_config_returns_deep_copy():
    a = Configuration(FormulaStub())
    a.set_random()
    b = Configuration(FormulaStub())
    b.from_config(a)
    assert a.evaluate_variable(1) == b.evaluate_variable(1)
    b.flip_variable(1)
    assert a.evaluate_variable(1) != b.evaluate_variable(1)