import pytest

from cpp_stats.metrics.number_of_classes import NumberOfClassesCalculator, NumberOfClassesMetric

def test_when_two_equal_classes_then_ignore_one():
    m1 = NumberOfClassesMetric(1)
    m2 = NumberOfClassesMetric(2)
    expected = 3

    _, actual = (m1 + m2).get()

    assert expected == actual
