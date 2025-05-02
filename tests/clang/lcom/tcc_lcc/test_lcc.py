import pytest
import pathlib

from cpp_stats.metrics.lcom.tcc_lcc.lcc import MeanLCCCalculator, MinLCCCalculator
from cpp_stats.ast.ast_tree import analyze_ast

import clang.cindex

EPS = 1e-5

def test_mean_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MEAN_LCC": MeanLCCCalculator()
        }
    )

    expected = (1/3 + 1) / 2

    _, actual = result["MEAN_LCC"].get()
    assert abs(expected - actual) < EPS

def test_min_metric_calculator(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/camc/",
        [pathlib.Path("./tests/data/analyze/lcom/lcom.hpp")],
        {
            "MIN_LCC": MinLCCCalculator()
        }
    )

    expected = 1/3

    _, actual = result["MIN_LCC"].get()
    assert abs(expected - actual) < EPS
