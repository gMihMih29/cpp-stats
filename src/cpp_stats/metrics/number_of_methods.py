'''
Module for MEAN_LENGTH_OF_METHODS and MAX_LENGTH_OF_METHODS metrics.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

MEAN_NUMBER_OF_METHODS_PER_CLASS = 'MEAN_NUMBER_OF_METHODS_PER_CLASS'
MAX_NUMBER_OF_METHODS_PER_CLASS = 'MAX_NUMBER_OF_METHODS_PER_CLASS'

def _merge_metric_data(lhv: dict[str, int], rhv: dict[str, int]):
    new_data = lhv
    for class_name, cnt in rhv.items():
        if new_data.get(class_name, None) is None:
            new_data[class_name] = cnt
        else:
            new_data[class_name] += cnt
    return rhv

class MeanNumberOfMethodsMetric(Metric):
    '''
    Represents MEAN_NUMBER_OF_METHODS_PER_CLASS metric.
    '''

    def __init__(self, data: dict[str, int]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, int]): data of metric. 
        keys are the names of classes, values - number of methods.
        '''
        super().__init__(MEAN_NUMBER_OF_METHODS_PER_CLASS)
        self._data = data

    def __add__(self, other):
        if not isinstance(other, MeanNumberOfMethodsMetric):
            raise NotImplementedError
        new_data = _merge_metric_data(self._data, other._data)
        return MeanNumberOfMethodsMetric(new_data)

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        sum_methods = 0
        cnt_classes = len(self._data)
        for _, cnt in self._data.items():
            sum_methods += cnt
        value = 0
        if cnt_classes != 0:
            value = sum / cnt_classes
        return MEAN_NUMBER_OF_METHODS_PER_CLASS, value

class MeanNumberOfMethodsCalculator(ClangMetricCalculator):
    '''
    Calculates MEAN_NUMBER_OF_METHODS_PER_CLASS.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MeanNumberOfMethodsMetric({})
        return MeanNumberOfMethodsMetric({node.semantic_parent.displayname: 1})

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return cursor.kind == clang.cindex.CursorKind.CXX_METHOD and cursor.is_definition()

class MaxNumberOfMethodsMetric(Metric):
    '''
    Represents MAX_NUMBER_OF_METHODS_PER_CLASS metric.
    '''

    def __init__(self, data: dict[str, int]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, int]): data of metric. 
        keys are the names of classes, values - number of methods.
        '''
        super().__init__(MAX_NUMBER_OF_METHODS_PER_CLASS)
        self._data = data

    def __add__(self, other):
        if not isinstance(other, MaxNumberOfMethodsMetric):
            raise NotImplementedError
        new_data = _merge_metric_data(self._data, other._data)
        return MaxNumberOfMethodsMetric(new_data)

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        max_value = 0
        for _, cnt in self._data.values():
            max_value = max(max_value, cnt)
        return MAX_NUMBER_OF_METHODS_PER_CLASS, max_value

class MaxNumberOfMethodsCalculator(ClangMetricCalculator):
    '''
    Calculates MAX_NUMBER_OF_METHODS_PER_CLASS.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MaxNumberOfMethodsMetric({})
        return MaxNumberOfMethodsMetric({node.semantic_parent.displayname: 1})

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return cursor.kind == clang.cindex.CursorKind.CXX_METHOD and cursor.is_definition()
