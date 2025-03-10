import pytest

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.number_of_classes import NumberOfClassesCalculator, NumberOfClassesMetric

import utils.clang

def test_when_add_two_noc_metrics_then_sum_values():
    m1 = NumberOfClassesMetric(1)
    m2 = NumberOfClassesMetric(2)
    expected = 3

    _, actual = (m1 + m2).get()

    assert expected == actual

def test_when_sum_with_unknown_metric_then_not_implemented():
    m1 = NumberOfClassesMetric(1)
    m2 = Metric("some metric")

    with pytest.raises(NotImplementedError):
        m1 + m2

@pytest.mark.skipif(
    (utils.clang.clang_index() is None),
    reason="Clang cannot be found using env variable LIBCLANG_LIBRARY_PATH"
)
def test_find_3_classes(clang_index):
    assert clang_index is not None
