'''
Tests module lines_of_code.py
'''
from pathlib import Path

from cpp_stats.metrics.lines_of_code import LinesOfCodeCalculator, LinesOfCodeMetric

def test_regular_1():
    files = [
        Path('./tests/data/repo/main.cpp')
    ]
    calculator = LinesOfCodeCalculator()
    expected = 6

    _, actual = calculator(files).get()

    assert expected == actual , f"Expected: {expected}, Actual: {actual}"
