import pytest
import pathlib

from cpp_stats.metrics.halstead.base import HalsteadData
from cpp_stats.metrics.halstead.base import create_data, merge_data
from cpp_stats.metrics.halstead.base import __get_binary_operator_spelling
from cpp_stats.metrics.halstead.base import __get_literal_spelling
from cpp_stats.metrics.halstead.base import __get_unary_operator_spelling
from cpp_stats.metrics.halstead.base import __find_remaining_operators
from cpp_stats.metrics.halstead.program_vocabulary import MeanHalsteadProgramVocabularyCalculator
from cpp_stats.ast.ast_tree import analyze_ast


import clang.cindex

@pytest.fixture
def distinct_operators_wiki():
    '''
    Returns distinct operators from wiki article about Halstead complexity
    https://en.wikipedia.org/wiki/Halstead_complexity_measures
    '''
    yield set(["main", "operator()", "{}", "int", "__isoc99_scanf", "operator&", "operator=", "operator+", "operator/", "printf", ",", ";"])

@pytest.fixture
def distinct_operands_wiki():
    '''
    Returns distinct operands from wiki article about Halstead complexity
    https://en.wikipedia.org/wiki/Halstead_complexity_measures
    '''
    yield set(["_ZZ4mainE1a", "_ZZ4mainE1b", "_ZZ4mainE1c", "_ZZ4mainE3avg", "\"%d %d %d\"", "3", "\"avg = %d\""])

EPS = 1e-5

def test_sum_data_happy_path():
    h1 = HalsteadData(set(['n1', 'n2']), set(['n1', 'n2']), 2, 2)
    h2 = HalsteadData(set(['n3', 'n2']), set(['n3', 'n2']), 2, 2)

    h3 = h1 + h2

    assert len(h3.n1) == 3
    assert len(h3.n2) == 3
    assert h3.N1 == 4
    assert h3.N2 == 4

def test_sum_halstead_data_not_implemented():
    h1 = HalsteadData(set(['n1', 'n2']), set(['n1', 'n2']), 2, 2)
    h2 = 3

    with pytest.raises(NotImplementedError):
        h1 + h2

def test_program_vocabulary(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 19

    actual = h.program_vocabulary()

    assert expected == actual

def test_program_length(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 42

    actual = h.program_length()

    assert expected == actual

def test_estimated_length(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 62.67103446

    actual = h.estimated_length()

    assert abs(expected - actual) < EPS

def test_volume(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 178.4129556

    actual = h.volume()

    assert abs(expected - actual) < EPS

def test_difficulty(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 12.85714286

    actual = h.difficulty()

    assert abs(expected - actual) < EPS

def test_effort(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 2293.880857

    actual = h.effort()

    assert abs(expected - actual) < EPS

def test_time_required_to_program(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 127.4378254

    actual = h.time_required_to_program()

    assert abs(expected - actual) < EPS

def test_number_of_delivered_bugs(distinct_operators_wiki, distinct_operands_wiki):
    number_of_operators = 27
    number_of_operands = 15
    h = HalsteadData(
        distinct_operators_wiki,
        distinct_operands_wiki,
        number_of_operators,
        number_of_operands
    )
    expected = 0.0594709852

    actual = h.delivered_bugs()

    assert abs(expected - actual) < EPS

def test_merge_data():
    h1 = HalsteadData(set(['n1', 'n2']), set(['n1', 'n2']), 2, 2)
    h2 = HalsteadData(set(['n3', 'n2']), set(['n3', 'n2']), 2, 2)
    h3 = HalsteadData(set(['n1', 'n3']), set(['n1', 'n3']), 2, 2)
    d1 = {
        "file1": h1,
        "file2": h2,
    }
    d2 = {
        "file1": h3,
        "file3": h2,
    }
    expected = {
        "file1": HalsteadData(set(['n1', 'n2', 'n3']), set(['n1', 'n2', 'n3']), 4, 4),
        "file2": h2,
        "file3": h2
    }

    actual = merge_data(d1, d2)

    assert expected['file1'].__dict__ == actual['file1'].__dict__
    assert expected['file2'].__dict__ == actual['file2'].__dict__
    assert expected['file3'].__dict__ == actual['file3'].__dict__

def test_get_binary_operator_spelling_1(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/halstead/spelling/binary_operator_1.hpp",
                           args=['-x', 'c++'])
    target = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.BINARY_OPERATOR:
            target = child
            break
    if target is None:
        assert False
    expected = "+"

    actual = __get_binary_operator_spelling(target)

    assert expected == actual

def test_get_binary_operator_spelling_2(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/halstead/spelling/binary_operator_2.hpp",
                           args=['-x', 'c++'])
    target = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
            target = child
            break
    if target is None:
        assert False
    expected = "^="

    actual = __get_binary_operator_spelling(target)

    assert expected == actual

def test_get_literal_spelling(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/halstead/spelling/literal.hpp",
                        args=['-x', 'c++'])
    target = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.STRING_LITERAL:
            target = child
            break
    if target is None:
        assert False
    expected = "\"HELLO WORLD\""

    actual = __get_literal_spelling(target)

    assert expected == actual

def test_get_unary_operator_spelling_1(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/halstead/spelling/unary_operator_1.hpp",
                        args=['-x', 'c++'])
    target = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.UNARY_OPERATOR:
            target = child
            break
    if target is None:
        assert False
    expected = "!"

    actual = __get_unary_operator_spelling(target)

    assert expected == actual

def test_get_unary_operator_spelling_2(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/halstead/spelling/unary_operator_2.hpp",
                        args=['-x', 'c++'])
    target = None
    for child in tu.cursor.walk_preorder():
        if child.kind == clang.cindex.CursorKind.UNARY_OPERATOR:
            target = child
            break
    if target is None:
        assert False
    expected = "+"

    actual = __get_unary_operator_spelling(target)

    assert expected == actual

def test_find_remaining_operators_wiki(clang_index: clang.cindex.Index):
    tu = clang_index.parse("./tests/data/analyze/halstead/wiki/wiki.hpp",
                        args=['-x', 'c++'])
    target = None
    for child in tu.cursor.walk_preorder():
        if (child.kind == clang.cindex.CursorKind.FUNCTION_DECL
            and child.spelling == "main"):
            target = child
            break
    if target is None:
        assert False
    expected_number_of_operators_1 = 11

    actual = __find_remaining_operators(target)

    assert expected_number_of_operators_1 == actual.N1

def test_create_data_wiki(clang_index: clang.cindex.Index, distinct_operators_wiki, distinct_operands_wiki):
    result = analyze_ast(
        clang_index,
        [pathlib.Path("./tests/data/analyze/halstead/wiki/wiki.hpp")],
        {
            "MEAN_HALSTEAD_PROGRAM_VOCABULARY": MeanHalsteadProgramVocabularyCalculator()
        }
    )
    expected_number_of_operators = 27
    expected_number_of_operands = 15

    halstead_data = result["MEAN_HALSTEAD_PROGRAM_VOCABULARY"]._data["tests/data/analyze/halstead/wiki/wiki.hpp"]
    assert halstead_data.n1 == distinct_operators_wiki
    assert halstead_data.n2 == distinct_operands_wiki
    assert halstead_data.N1 == expected_number_of_operators
    assert halstead_data.N2 == expected_number_of_operands
