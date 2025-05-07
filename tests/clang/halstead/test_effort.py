import pytest
import clang.cindex
import pathlib

from cpp_stats.metrics.halstead.effort import MeanHalsteadEffortCalculator, MaxHalsteadEffortCalculator
from cpp_stats.ast.ast_tree import analyze_ast

EPS = 1e-5

def test_mean_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MEAN_HALSTEAD_EFFORT": MeanHalsteadEffortCalculator()
        }
    )
    expected = 2293.880857

    _, actual = result["MEAN_HALSTEAD_EFFORT"].get()
    assert abs(expected - actual) < EPS

def test_max_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MAX_HALSTEAD_EFFORT": MaxHalsteadEffortCalculator()
        }
    )
    expected = 2293.880857

    _, actual = result["MAX_HALSTEAD_EFFORT"].get()
    assert abs(expected - actual) < EPS
