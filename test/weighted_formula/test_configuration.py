
from weighted_formula.configuration import Configuration
from weighted_formula.weighted_formula import WeightedCnf


def test_from_config_returns_deep_copy():
    a = Configuration(WeightedCnf([(1,2,3)], (5, 7, 8)))
    a.set_random()
    b = Configuration(WeightedCnf([(1,2,3)], (5, 7, 8)))
    b.from_config(a)
    assert a.evaluate_variable(1) == b.evaluate_variable(1)
    b.flip_variable(1)
    assert a.evaluate_variable(1) != b.evaluate_variable(1)