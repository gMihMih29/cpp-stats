import pytest
import pathlib

from cpp_stats.metrics.lcom.lcom3 import MeanLCOM3Calculator, MaxLCOM3Calculator
from cpp_stats.ast.ast_tree import analyze_ast

import clang.cindex

EPS = 1e-5

def test_mean_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MEAN_LCOM3": MeanLCOM3Calculator()
        }
    )

    expected = (13/12 + 7/6) / 2

    _, actual = result["MEAN_LCOM3"].get()
    assert abs(expected - actual) < EPS

def test_max_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MAX_LCOM3": MaxLCOM3Calculator()
        }
    )

    expected = 7/6

    _, actual = result["MAX_LCOM3"].get()
    assert abs(expected - actual) < EPS
