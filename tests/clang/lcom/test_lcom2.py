import pytest
import pathlib

from cpp_stats.metrics.lcom.lcom2 import MeanLCOM2Calculator, MaxLCOM2Calculator
from cpp_stats.ast.ast_tree import analyze_ast

import clang.cindex

EPS = 1e-5

def test_mean_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MEAN_LCOM2": MeanLCOM2Calculator()
        }
    )

    expected = (1/4 + 1/2) / 2

    _, actual = result["MEAN_LCOM2"].get()
    assert abs(expected - actual) < EPS

def test_max_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MAX_LCOM2": MaxLCOM2Calculator()
        }
    )

    expected = 1/2

    _, actual = result["MAX_LCOM2"].get()
    assert abs(expected - actual) < EPS
