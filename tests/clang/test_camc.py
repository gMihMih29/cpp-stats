import pytest
import pathlib

from cpp_stats.metrics.camc import MeanCAMCCalculator, MinCAMCCalculator, MaxCAMCCalculator
from cpp_stats.ast.ast_tree import analyze_ast

import clang.cindex

EPS = 1e-5

def test_mean_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/camc/camc.hpp")],
        {
            "MEAN_CAMC": MeanCAMCCalculator()
        }
    )

    expected = (1/3 + 5/9) / 2

    _, actual = result["MEAN_CAMC"].get()
    assert abs(expected - actual) < EPS

def test_max_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/camc/camc.hpp")],
        {
            "MAX_CAMC": MaxCAMCCalculator()
        }
    )

    expected = 5/9

    _, actual = result["MAX_CAMC"].get()
    assert abs(expected - actual) < EPS

def test_min_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/camc/camc.hpp")],
        {
            "MIN_CAMC": MinCAMCCalculator()
        }
    )

    expected = 1/3

    _, actual = result["MIN_CAMC"].get()
    assert abs(expected - actual) < EPS
