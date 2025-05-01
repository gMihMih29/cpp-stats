import pytest
import pathlib

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.maintainability_index import MeanMaintainabilityIndexCalculator, MinMaintainabilityIndexCalculator
from cpp_stats.metrics.maintainability_index import MeanMaintainabilityIndexMetric, MinMaintainabilityIndexMetric
from cpp_stats.metrics.maintainability_index import MeanHalsteadVolumeMetric, MeanCyclomaticComplexityMetric
from cpp_stats.metrics.maintainability_index import _merge_data
from cpp_stats.metrics.halstead.base import HalsteadData
from cpp_stats.ast.ast_tree import analyze_ast

import clang.cindex

EPS = 1e-5

def test_merge_data():
    lhv = {
        "file1": (
            10,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        ),
        "file2": (
            100,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        )
    }
    rhv = {
        "file1": (
            10,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n3", "n4"}, {"n3", "n4"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(15, 1)
        ),
        "file3": (
            100,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        )
    }
    expected = {
        "file1": (
            20,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2", "n3", "n4"}, {"n1", "n2", "n3", "n4"}, 6, 8)
            }),
            MeanCyclomaticComplexityMetric(25, 2)
        ),
        "file2": (
            100,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        ),
        "file3": (
            100,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        )
    }

    actual = _merge_data(lhv, rhv)

    for key, item in expected.items():
        loc_expected, vol_expected, cycl_expected = item
        loc_actual, vol_actual, cycl_actual = actual[key]
        assert loc_expected == loc_actual
        assert vol_expected.data["file1"].n1 == vol_actual.data["file1"].n1
        assert vol_expected.data["file1"].n2 == vol_actual.data["file1"].n2
        assert vol_expected.data["file1"].N1 == vol_actual.data["file1"].N1
        assert vol_expected.data["file1"].N2 == vol_actual.data["file1"].N2
        assert cycl_expected.sum_value == cycl_actual.sum_value

def test_get_max_metric():
    metric = MinMaintainabilityIndexMetric({
        "file1": (
            10,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        ),
        "file2": (
            100,
            MeanHalsteadVolumeMetric({
                "file2": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        )
    })
    expected = 80.37314487

    _, actual = metric.get()

    assert abs(expected - actual) < EPS

def test_get_mean_metric():
    metric = MeanMaintainabilityIndexMetric({
        "file1": (
            10,
            MeanHalsteadVolumeMetric({
                "file1": HalsteadData({"n1", "n2"}, {"n1", "n2"}, 3, 4)
            }),
            MeanCyclomaticComplexityMetric(10, 1)
        )
    })
    expected = 117.6750234

    _, actual = metric.get()

    assert abs(expected - actual) < EPS

def test_min_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MIN_MAINTAINABILITY_INDEX": MinMaintainabilityIndexCalculator()
        }
    )

    expected = 106.5107971

    _, actual = result["MIN_MAINTAINABILITY_INDEX"].get()
    assert abs(expected - actual) < EPS

def test_mean_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MEAN_MAINTAINABILITY_INDEX": MeanMaintainabilityIndexCalculator()
        }
    )

    expected = 106.5107971

    _, actual = result["MEAN_MAINTAINABILITY_INDEX"].get()
    assert abs(expected - actual) < EPS
