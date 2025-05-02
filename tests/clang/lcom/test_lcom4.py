import pytest
import pathlib

from cpp_stats.metrics.lcom.lcom4 import MeanLCOM4Calculator, MaxLCOM4Calculator
from cpp_stats.ast.ast_tree import analyze_ast

import clang.cindex

EPS = 1e-5

def test_mean_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MEAN_LCOM4": MeanLCOM4Calculator()
        }
    )

    expected = (2 + 1) / 2

    _, actual = result["MEAN_LCOM4"].get()
    assert abs(expected - actual) < EPS

def test_max_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MAX_LCOM4": MaxLCOM4Calculator()
        }
    )

    expected = 2

    _, actual = result["MAX_LCOM4"].get()
    assert abs(expected - actual) < EPS
