import pytest
import clang.cindex
import pathlib

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.halstead.program_vocabulary import MeanHalsteadProgramVocabularyCalculator, MaxHalsteadProgramVocabularyCalculator
from cpp_stats.metrics.halstead.program_vocabulary import MeanHalsteadProgramVocabularyMetric, MaxHalsteadProgramVocabularyMetric
from cpp_stats.metrics.halstead.base import HalsteadData
from cpp_stats.ast.ast_tree import analyze_ast

def test_when_sum_with_unknown_metric_then_not_implemented():
    m1 = MeanHalsteadProgramVocabularyMetric({})
    m2 = Metric("some metric")

    with pytest.raises(NotImplementedError):
        m1 + m2

def test_get_mean_metric():
    metric = MeanHalsteadProgramVocabularyMetric(
        {
            "file1": HalsteadData(set(['n1', 'n2']), set(['n1', 'n2']), 2, 2)
        }
    )
    expected = 4

    _, actual = metric.get()

    assert expected == actual

def test_get_max_metric():
    metric = MaxHalsteadProgramVocabularyMetric(
        {
            "file1": HalsteadData(set(['n1', 'n2']), set(['n1', 'n2']), 2, 2),
            "file2": HalsteadData(set(['n1', 'n2', 'n3', 'n4']), set(['n1', 'n2']), 2, 2),
        }
    )
    expected = 6

    _, actual = metric.get()

    assert expected == actual

def test_mean_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MEAN_HALSTEAD_PROGRAM_VOCABULARY": MeanHalsteadProgramVocabularyCalculator()
        }
    )
    expected = 19

    _, actual = result["MEAN_HALSTEAD_PROGRAM_VOCABULARY"].get()
    assert expected == actual

def test_max_wiki(clang_index: clang.cindex.Index):
    result = analyze_ast(
        clang_index,
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MAX_HALSTEAD_PROGRAM_VOCABULARY": MaxHalsteadProgramVocabularyCalculator()
        }
    )
    expected = 19

    _, actual = result["MAX_HALSTEAD_PROGRAM_VOCABULARY"].get()
    assert expected == actual
