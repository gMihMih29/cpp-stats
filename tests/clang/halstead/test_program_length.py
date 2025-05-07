import pytest
import clang.cindex
import pathlib

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.halstead.program_length import MeanHalsteadProgramLengthCalculator, MaxHalsteadProgramLengthCalculator
from cpp_stats.metrics.halstead.program_length import MeanHalsteadProgramLengthMetric, MaxHalsteadProgramLengthMetric
from cpp_stats.ast.ast_tree import analyze_ast

def test_create_data_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MEAN_HALSTEAD_PROGRAM_LENGTH": MeanHalsteadProgramLengthCalculator()
        }
    )
    expected = 42

    _, actual = result["MEAN_HALSTEAD_PROGRAM_LENGTH"].get()
    assert expected == actual

def test_max_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        "./tests/data/analyze/halstead/wiki/",
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MAX_HALSTEAD_PROGRAM_LENGTH": MaxHalsteadProgramLengthCalculator()
        }
    )
    expected = 42

    _, actual = result["MAX_HALSTEAD_PROGRAM_LENGTH"].get()
    assert expected == actual
