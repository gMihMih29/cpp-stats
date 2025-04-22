import pytest
import clang.cindex
import pathlib

from cpp_stats.metrics.halstead.program_length import MeanHalsteadProgramLengthCalculator, MaxHalsteadProgramLengthCalculator
from cpp_stats.ast.ast_tree import analyze_ast

EPS = 1e-5

def test_mean_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MEAN_HALSTEAD_PROGRAM_LENGTH": MeanHalsteadProgramLengthCalculator()
        }
    )
    expected = 42

    _, actual = result["MEAN_HALSTEAD_PROGRAM_LENGTH"].get()
    assert abs(expected - actual) < EPS

def test_max_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MAX_HALSTEAD_PROGRAM_LENGTH": MaxHalsteadProgramLengthCalculator()
        }
    )
    expected = 42

    _, actual = result["MAX_HALSTEAD_PROGRAM_LENGTH"].get()
    assert abs(expected - actual) < EPS
