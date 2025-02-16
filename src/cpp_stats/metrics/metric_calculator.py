'''
Base classes for metrics and calculators.
'''

from pathlib import Path

import clang.cindex

class Metric:
    '''
    Class that stores metric name and value.
    '''

    def __add__(self, other):
        pass

    def get(self):
        '''
        Returns metric value. Should be called since metric can be summarization of many files,
        namespaces, classes and etc.
        '''

class BasicMetricCalculator:
    '''
    Class for calculating specific list of metrics.
    '''

    def __call__(self, file_paths: list[Path]) -> list[Metric]:
        '''
        Calculates metrics for a given set of C/C++ files.

        Parameters:
        file_paths (list[Path]): paths to C/C++ files

        Returns:
        list[Metric]: List of metrics calculated for set of files.
        '''

class ClangMetricCalculator:
    '''
    Class for calculating specific list of metrics.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> list[Metric]:
        '''
        Calculates metrics for a given node that represents function, 
        method, class or etc.

        Parameters:
        node (clang.cindex.Cursor): Node for which metrics are 
        calculated.

        Returns:
        list[Metric]: List of metrics calculated for node.
        '''

    def observed_cursors(self) -> list[clang.cindex.CursorKind]:
        '''
        Returns list of cursor kinds that can be passed as an argument 
        for __call__.

        Returns:
        list[clang.cindex.CursorKind]: List of observed cursor kinds.
        '''
