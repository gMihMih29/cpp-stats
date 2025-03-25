import pytest

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.length_of_method import MeanLengthOfMethodsCalculator, MaxLengthOfMethodsCalculator, _length_of_method
from cpp_stats.metrics.length_of_method import MeanLengthOfMethodsMetric, MaxLengthOfMethodsMetric

import clang.cindex

def test_when_add_two_mean_metrics_then_sum_values():
    m1 = MeanLengthOfMethodsMetric(1, 1)
    m2 = MeanLengthOfMethodsMetric(2, 1)
    expected_length = 3
    expected_cnt = 2

    m3 = m1 + m2

    assert expected_length == m3.length
    assert expected_cnt == m3.cnt

def test_happy_path_get_mean_lom_value():
    m = MeanLengthOfMethodsMetric(2000, 1)
    expected = 2000

    _, actual = m.get()

    assert expected == actual

def test_zero_methods_get_mean_lom_value():
    m = MeanLengthOfMethodsMetric(0, 0)
    expected = 0

    _, actual = m.get()

    assert expected == actual

def test_when_sum_with_unknown_metric_then_not_implemented_1():
    m1 = MeanLengthOfMethodsMetric(1, 1)
    m2 = Metric("some metric")

    with pytest.raises(NotImplementedError):
        m1 + m2

def test_when_add_two_max_metrics_then_max_value_is_stored():
    m1 = MaxLengthOfMethodsMetric(1)
    m2 = MaxLengthOfMethodsMetric(2000)
    expected = 2000

    actual = (m1 + m2).length

    assert expected == actual

def test_when_sum_with_unknown_metric_then_not_implemented_2():
    m1 = MaxLengthOfMethodsMetric(1)
    m2 = Metric("some metric")

    with pytest.raises(NotImplementedError):
        m1 + m2

def test_happy_path_get_max_lom_value():
    m = MaxLengthOfMethodsMetric(2000)
    expected = 2000

    _, actual = m.get()

    assert expected == actual

def test_happy_path_calculate_length_of_method(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
    method = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method2()":
            method = child
            break
    if method is None:
        assert False
    expected = 7

    actual = _length_of_method(method)

    assert expected == actual

def test_one_line_calculate_length_of_method(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
    method = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method3()":
            method = child
            break
    if method is None:
        assert False
    expected = 1

    actual = _length_of_method(method)

    assert expected == actual

def test_happy_path_mean_calculator(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
    calc = MeanLengthOfMethodsCalculator()
    method = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method2()":
            method = child
            break
    if method is None:
        assert False
    expected = 7

    _, actual = calc(method).get()

    assert expected == actual

def test_declaration_mean_calculator(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
    calc = MeanLengthOfMethodsCalculator()
    method = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method1()":
            method = child
            break
    if method is None:
        assert False
    expected = 0

    _, actual = calc(method).get()

    assert expected == actual

def test_happy_path_max_calculator(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
    calc = MaxLengthOfMethodsCalculator()
    method = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method2()":
            method = child
            break
    if method is None:
        assert False
    expected = 7

    _, actual = calc(method).get()

    assert expected == actual

def test_declaration_max_calculator(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
    calc = MaxLengthOfMethodsCalculator()
    method = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method1()":
            method = child
            break
    if method is None:
        assert False
    expected = 0

    _, actual = calc(method).get()

    assert expected == actual
