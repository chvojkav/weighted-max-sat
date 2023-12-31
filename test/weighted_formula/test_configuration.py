
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

def test_sat_literals_counts():
    a = Configuration(WeightedCnf([(1,2,3), (-1, -2, -3)], (5, 7, 8)))
    a.set_random()
    assert a.counts_of_satisfied_literals[0] == (
        a.evaluate_variable(1) + a.evaluate_variable(2) + a.evaluate_variable(3)
    )
    a.set_variable(1, True)
    a.set_variable(2, True)
    a.set_variable(3, True)
    assert a.counts_of_satisfied_literals[0] == 3
    assert a.counts_of_satisfied_literals[1] == 0
    a.set_variable(1, False)
    assert a.counts_of_satisfied_literals[0] == 2
    assert a.counts_of_satisfied_literals[1] == 1
    a.set_variable(2, False)
    assert a.counts_of_satisfied_literals[0] == 1
    assert a.counts_of_satisfied_literals[1] == 2
    a.set_variable(3, False)
    assert a.counts_of_satisfied_literals[0] == 0
    assert a.counts_of_satisfied_literals[1] == 3
    a.flip_variable(1)
    assert a.counts_of_satisfied_literals[0] == 1
    assert a.counts_of_satisfied_literals[1] == 2
    a.flip_variable(2)
    assert a.counts_of_satisfied_literals[0] == 2
    assert a.counts_of_satisfied_literals[1] == 1
    a.flip_variable(3)
    assert a.counts_of_satisfied_literals[0] == 3
    assert a.counts_of_satisfied_literals[1] == 0

def test_weights():
    a = Configuration(WeightedCnf([(1,2,3), (-1, -2, -3)], (5, 7, 8)))
    a.set_random()
    a.set_variable(1, True)
    a.set_variable(2, True)
    a.set_variable(3, True)
    assert a.sat_weights_sum == 20
    a.set_variable(1, False)
    assert a.sat_weights_sum == 15
    a.set_variable(2, False)
    assert a.sat_weights_sum == 8
    a.set_variable(3, False)
    assert a.sat_weights_sum == 0
    a.flip_variable(1)
    assert a.sat_weights_sum == 5
    a.flip_variable(2)
    assert a.sat_weights_sum == 12
    a.flip_variable(3)
    assert a.sat_weights_sum == 20
