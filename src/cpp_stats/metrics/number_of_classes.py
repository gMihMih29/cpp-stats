'''
Module for NUMBER_OF_CLASSES metric.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

METRIC_NAME = 'NUMBER_OF_CLASSES'

class NumberOfClassesMetric(Metric):
    '''
    Represents NUMBER_OF_CLASSES metric.
    '''

    def __init__(self, value: int):
        '''
        Initializes metric.
        
        Parameters:
        value (float): Metric value.
        '''
        super().__init__(METRIC_NAME)
        self.value = value

    def __add__(self, other):
        if not isinstance(other, NumberOfClassesMetric):
            raise NotImplementedError
        return NumberOfClassesMetric(self.value + other.value)

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        return METRIC_NAME, self.value

class NumberOfClassesCalculator(ClangMetricCalculator):
    '''
    Calculates NUMBER_OF_CLASSES.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return NumberOfClassesMetric(0)
        return NumberOfClassesMetric(1)

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return cursor.kind == clang.cindex.CursorKind.CLASS_DECL and cursor.is_definition()
                