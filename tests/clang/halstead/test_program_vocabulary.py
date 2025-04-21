import pytest

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.halstead.program_vocabulary import MeanHalsteadProgramVocabularyCalculator, MaxHalsteadProgramVocabularyCalculator
from cpp_stats.metrics.halstead.program_vocabulary import MeanHalsteadProgramVocabularyMetric, MaxHalsteadProgramVocabularyMetric

import clang.cindex

# def test_when_sum_with_unknown_metric_then_not_implemented_2():
#     m1 = MaxCyclomaticComplexityMetric(100)
#     m2 = Metric("some metric")

#     with pytest.raises(NotImplementedError):
#         m1 + m2

# def test_calculate_complexity_sum_of_primes(clang_index: clang.cindex.Index):
#     tu = clang_index.parse("./tests/data/analyze/cyclomatic_complexity.hpp", args=['-x', 'c++'])
#     func = None
#     for child in tu.cursor.walk_preorder():
#         if (child.kind == clang.cindex.CursorKind.FUNCTION_DECL
#             and child.displayname == "test1(int, int)"):
#             func = child
#             break
#     if func is None:
#         assert False
#     expected = 3

#     actual = _calculate_cyclomatic_complexity(func)

#     assert expected == actual