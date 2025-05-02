import pytest
import pathlib

from cpp_stats.metrics.arg_types.nhd import MeanNHDCalculator, MinNHDCalculator, MaxNHDCalculator
from cpp_stats.ast.ast_tree import analyze_ast

import clang.cindex

EPS = 1e-5

def test_mean_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/camc/camc.hpp")],
        {
            "MEAN_NHD": MeanNHDCalculator()
        }
    )

    expected = (2/9 + 0) / 2

    _, actual = result["MEAN_NHD"].get()
    assert abs(expected - actual) < EPS

def test_max_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/camc/camc.hpp")],
        {
            "MAX_NHD": MaxNHDCalculator()
        }
    )

    expected = 2/9

    _, actual = result["MAX_NHD"].get()
    assert abs(expected - actual) < EPS

def test_min_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/camc/camc.hpp")],
        {
            "MIN_NHD": MinNHDCalculator()
        }
    )

    expected = 0

    _, actual = result["MIN_NHD"].get()
    assert abs(expected - actual) < EPS
