import pytest
import clang.cindex
import pathlib

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.halstead.volume import MeanHalsteadVolumeCalculator, MaxHalsteadVolumeCalculator
from cpp_stats.metrics.halstead.volume import MeanHalsteadVolumeMetric, MaxHalsteadVolumeMetric
from cpp_stats.metrics.halstead.base import HalsteadData
from cpp_stats.ast.ast_tree import analyze_ast

EPS = 1e-5

def test_when_sum_with_unknown_metric_then_not_implemented():
    m1 = MeanHalsteadVolumeMetric({})
    m2 = Metric("some metric")

    with pytest.raises(NotImplementedError):
        m1 + m2

def test_mean_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MEAN_HALSTEAD_VOLUME": MeanHalsteadVolumeCalculator()
        }
    )
    expected = 178.4129556

    _, actual = result["MEAN_HALSTEAD_VOLUME"].get()
    assert abs(expected - actual) < EPS

def test_max_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MAX_HALSTEAD_VOLUME": MaxHalsteadVolumeCalculator()
        }
    )
    expected = 178.4129556

    _, actual = result["MAX_HALSTEAD_VOLUME"].get()
    assert abs(expected - actual) < EPS
