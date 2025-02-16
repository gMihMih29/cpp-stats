'''
Main class for calculating metrics.
'''

from pathlib import Path

from cpp_stats.metrics.lines_of_code import LinesOfCodeCalculator
from cpp_stats.metrics.metric_calculator import Metric

class CodeAnalyzer:
    '''
    Provides calculated metrics.
    '''

    def __init__(self, c_cxx_files: list[Path], use_clang: bool = False):
        self._files = c_cxx_files
        self._use_clang = use_clang
        self._ast_tree = None
        if use_clang:
            self._ast_tree = None
        self._basic_calculators = {
            'LINES_OF_CODE' : LinesOfCodeCalculator(),
        }
        self._clang_calculators = {
            'NUMBER_OF_CLASSES' : None,
        }
        self._cache = {
            'LINES_OF_CODE' : None,
            'NUMBER_OF_CLASSES' : None,
        }

    def metric(self, metric_name: str) -> Metric | None:
        '''
        Returns calculated metric by name.
        
        Parameters:
        metric_name (str): Metric name.
        '''
        if self._cache[metric_name] is not None:
            return self._cache[metric_name]
        if self._basic_calculators[metric_name] is not None:
            self._cache[metric_name] = self._basic_calculators[metric_name](self._files)
        if self._use_clang and self._clang_calculators[metric_name] is not None:
            self._cache[metric_name] = self._clang_calculators[metric_name](self._ast_tree)
        return self._cache.get(metric_name, (None, None))
