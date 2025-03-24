import pytest

from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.metrics.number_of_methods import MeanNumberOfMethodsCalculator, MaxNumberOfMethodsCalculator
from cpp_stats.metrics.number_of_methods import MeanNumberOfMethodsMetric, MaxNumberOfMethodsMetric, _merge_metric_data

import clang.cindex

def test_merge_mean_metric_data():
    m1 = MeanNumberOfMethodsMetric({
        'name1': 1,
        'name2': 2,
    })
    m2 = MeanNumberOfMethodsMetric({
        'name1': 3,
        'name3': 1
    })
    expected = {
        'name1': 4,
        'name2': 2,
        'name3': 1
    }

    actual = (m1 + m2)._data

    assert expected == actual

def test_merge_max_metric_data():
    m1 = MaxNumberOfMethodsMetric({
        'name1': 1,
        'name2': 2,
    })
    m2 = MaxNumberOfMethodsMetric({
        'name1': 3,
        'name3': 1
    })
    expected = {
        'name1': 4,
        'name2': 2,
        'name3': 1
    }

    actual = (m1 + m2)._data

    assert expected == actual

def test_when_sum_with_unknown_metric_then_not_implemented_1():
    m1 = MeanNumberOfMethodsMetric({})
    m2 = Metric("some metric")

    with pytest.raises(NotImplementedError):
        m1 + m2

def test_when_sum_with_unknown_metric_then_not_implemented_2():
    m1 = MaxNumberOfMethodsMetric({})
    m2 = Metric("some metric")

    with pytest.raises(NotImplementedError):
        m1 + m2

def test_happy_path_get_mean_metric():
    m = MeanNumberOfMethodsMetric({
        'name1': 1,
        'name2': 2,
    })
    expected = 1.5

    _, actual = m.get()

    assert expected == actual

def test_empty_data_get_mean_metric():
    m = MeanNumberOfMethodsMetric({
    })
    expected = 0

    _, actual = m.get()

    assert expected == actual

def test_happy_path_get_max_metric():
    m = MaxNumberOfMethodsMetric({
        'name1': 1,
        'name2': 2,
    })
    expected = 2

    _, actual = m.get()

    assert expected == actual

def test_happy_path_save_info_about_method_for_mean(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/number_of_methods.hpp", args=['-x', 'c++'])
    method = None
    calc = MeanNumberOfMethodsCalculator()
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method1()":
            method = child
            break
    if method is None:
        assert False
    expected = {
        '::C1': 1
    }

    actual = calc(method)._data

    assert expected == actual

def test_not_valid_cursor_for_mean(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/number_of_methods.hpp", args=['-x', 'c++'])
    cls = None
    calc = MeanNumberOfMethodsCalculator()
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CLASS_DECL and child.displayname == "C1":
            cls = child
            break
    if cls is None:
        assert False
    expected = {
    }

    actual = calc(cls)._data

    assert expected == actual

def test_happy_path_save_info_about_method_for_max(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/number_of_methods.hpp", args=['-x', 'c++'])
    method = None
    calc = MaxNumberOfMethodsCalculator()
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method1()":
            method = child
            break
    if method is None:
        assert False
    expected = {
        '::C1': 1
    }

    actual = calc(method)._data

    assert expected == actual

def test_not_valid_cursor_for_max(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/number_of_methods.hpp", args=['-x', 'c++'])
    cls = None
    calc = MaxNumberOfMethodsCalculator()
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.CLASS_DECL and child.displayname == "C1":
            cls = child
            break
    if cls is None:
        assert False
    expected = {
    }

    actual = calc(cls)._data

    assert expected == actual

# def test_one_line_calculate_length_of_method(clang_index: clang.cindex.Index):
#     tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
#     method = None
#     for child in tu.cursor.walk_preorder():
#         if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method3()":
#             method = child
#             break
#     if method is None:
#         assert False
#     expected = 1

#     actual = _length_of_method(method)

#     assert expected == actual

# def test_happy_path_mean_calculator(clang_index: clang.cindex.Index):
#     tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
#     calc = MeanLengthOfMethodsCalculator()
#     method = None
#     for child in tu.cursor.walk_preorder():
#         if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method2()":
#             method = child
#             break
#     if method is None:
#         assert False
#     expected = 7

#     _, actual = calc(method).get()

#     assert expected == actual

# def test_declaration_mean_calculator(clang_index: clang.cindex.Index):
#     tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
#     calc = MeanLengthOfMethodsCalculator()
#     method = None
#     for child in tu.cursor.walk_preorder():
#         if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method1()":
#             method = child
#             break
#     if method is None:
#         assert False
#     expected = 0

#     _, actual = calc(method).get()

#     assert expected == actual

# def test_happy_path_max_calculator(clang_index: clang.cindex.Index):
#     tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
#     calc = MaxLengthOfMethodsCalculator()
#     method = None
#     for child in tu.cursor.walk_preorder():
#         if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method2()":
#             method = child
#             break
#     if method is None:
#         assert False
#     expected = 7

#     _, actual = calc(method).get()

#     assert expected == actual

# def test_declaration_max_calculator(clang_index: clang.cindex.Index):
#     tu = clang_index.parse("./tests/data/analyze/methods.hpp", args=['-x', 'c++'])
#     calc = MaxLengthOfMethodsCalculator()
#     method = None
#     for child in tu.cursor.walk_preorder():
#         if child.kind == clang.cindex.CursorKind.CXX_METHOD and child.displayname == "method1()":
#             method = child
#             break
#     if method is None:
#         assert False
#     expected = 0

#     _, actual = calc(method).get()

#     assert expected == actual
