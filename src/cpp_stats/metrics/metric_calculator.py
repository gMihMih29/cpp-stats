from pathlib import Path

import clang.cindex

from cpp_stats.metrics.metric import Metric

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

        pass

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

        pass

    def observed_cursors(self) -> list[clang.cindex.CursorKind]:
        '''
        Returns list of cursor kinds that can be passed as an argument 
        for __call__.

        Returns:
        list[clang.cindex.CursorKind]: List of observed cursor kinds.
        '''

        pass
