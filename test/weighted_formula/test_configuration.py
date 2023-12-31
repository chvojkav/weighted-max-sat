
from weighted_formula.configuration import Configuration
from copy import copy

def test_from_config_returns_deep_copy():
    a = Configuration(2)
    a.set_random()
    b = Configuration(2)
    b.from_config(a)
    assert a.evaluate_variable(1) == b.evaluate_variable(1)
    b.flip_variable(1)
    assert a.evaluate_variable(1) != b.evaluate_variable(1)