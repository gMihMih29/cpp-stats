'''
Tests for cpp_stats main class.
'''
from pathlib import Path

from cpp_stats.cpp_stats import CppStats

def test_number_of_c_cxx_files_1(repo: Path):
    stats = CppStats(str(repo))
    expected = 1

    actual = stats.metric('NUMBER_OF_C_C++_FILES')

    assert expected == actual

def test_number_of_c_cxx_files_2(repo_with_2gitignore: Path):
    stats = CppStats(str(repo_with_2gitignore))
    expected = 1

    actual = stats.metric('NUMBER_OF_C_C++_FILES')

    assert expected == actual

def test_number_of_c_cxx_files_3(repo_with_gitignore: Path):
    stats = CppStats(str(repo_with_gitignore))
    expected = 1

    actual = stats.metric('NUMBER_OF_C_C++_FILES')

    assert expected == actual


def test_number_of_c_cxx_files_4(repo_with_ignr_modules: Path):
    stats = CppStats(str(repo_with_ignr_modules))
    expected = 2

    actual = stats.metric('NUMBER_OF_C_C++_FILES')

    assert expected == actual
