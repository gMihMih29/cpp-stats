'''
Module for MEAN_LENGTH_OF_METHODS and MAX_LENGTH_OF_METHODS metrics.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

MEAN_LENGTH_OF_METHODS = 'MEAN_LENGTH_OF_METHODS'
MAX_LENGTH_OF_METHODS = 'MAX_LENGTH_OF_METHODS'

def _length_of_method(method: clang.cindex.Cursor):
    assert method.kind == clang.cindex.CursorKind.CXX_METHOD
    return method.extent.end.line - method.extent.start.line + 1

class MeanLengthOfMethodsMetric(Metric):
    '''
    Represents MEAN_LENGTH_OF_METHODS metric.
    '''

    def __init__(self, length: int, cnt: int):
        '''
        Initializes metric.
        
        Parameters:
        length (int): summarized length of methods.
        cnt (int): quantity of methods.
        '''
        super().__init__(MEAN_LENGTH_OF_METHODS)
        self.length = length
        self.cnt = cnt

    def __add__(self, other):
        if not isinstance(other, MeanLengthOfMethodsMetric):
            raise NotImplementedError
        return MeanLengthOfMethodsMetric(self.length + other.length, self.cnt + other.cnt)

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        value = 0
        if self.cnt != 0:
            value = self.length / self.cnt
        return MEAN_LENGTH_OF_METHODS, value

class MeanLengthOfMethodsCalculator(ClangMetricCalculator):
    '''
    Calculates MEAN_LENGTH_OF_METHODS.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MeanLengthOfMethodsMetric(0, 0)
        return MeanLengthOfMethodsMetric(_length_of_method(node), 1)

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return cursor.kind == clang.cindex.CursorKind.CXX_METHOD and cursor.is_definition()

class MaxLengthOfMethodsMetric(Metric):
    '''
    Represents MAX_LENGTH_OF_METHODS metric.
    '''

    def __init__(self, length: int):
        '''
        Initializes metric.
        
        Parameters:
        length (int): Max length of analyzed methods.
        '''
        super().__init__(MAX_LENGTH_OF_METHODS)
        self.length = length

    def __add__(self, other):
        if not isinstance(other, MaxLengthOfMethodsMetric):
            raise NotImplementedError
        return MaxLengthOfMethodsMetric(max(self.length, other.length))

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        return MAX_LENGTH_OF_METHODS, self.length

class MaxLengthOfMethodsCalculator(ClangMetricCalculator):
    '''
    Calculates MAX_LENGTH_OF_METHODS.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MaxLengthOfMethodsMetric(0)
        return MaxLengthOfMethodsMetric(_length_of_method(node))

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return cursor.kind == clang.cindex.CursorKind.CXX_METHOD and cursor.is_definition()
