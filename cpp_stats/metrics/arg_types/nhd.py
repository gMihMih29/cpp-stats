'''
Module for MEAN_NHD, MAX_NHD and MIN_NHD metrics.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

from cpp_stats.metrics.arg_types.base import merge_argument_data, get_argument_data

MEAN_NHD = 'MEAN_NHD'
MIN_NHD = 'MIN_NHD'
MAX_NHD = 'MAX_NHD'

def _calculate_nhd(methods: dict[str, set[str]]):
    all_types = set([])
    summ = 0
    for _, types in methods.items():
        all_types |= types
    if len(all_types) == 0 or len(methods) <= 1:
        return 0
    for method_name_lhv, types_lhv in methods.items():
        for method_name_rhv, types_rhv in methods.items():
            if method_name_lhv == method_name_rhv:
                continue
            summ += len(types_lhv.intersection(types_rhv))
    return summ / (len(methods) * (len(methods) - 1) * len(all_types))

class MeanNHDMetric(Metric):
    '''
    Represents MEAN_NHD metric.
    '''

    def __init__(self, data: dict[str, dict[str, set[str]]]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, dict[str, set[str]]]): dictionary that contains set of argument types for
        each viewed method for each viewed class
        '''
        super().__init__(MEAN_NHD)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MeanNHDMetric):
            raise NotImplementedError
        return MeanNHDMetric(merge_argument_data(self.data, other.data))

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        summ = 0
        n = len(self.data)
        if n == 0:
            return MEAN_NHD, 0
        for _, class_methods in self.data.items():
            summ += _calculate_nhd(class_methods)
        return MEAN_NHD, summ / n

class MeanNHDCalculator(ClangMetricCalculator):
    '''
    Calculates MEAN_NHD.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MeanNHDMetric({})
        return MeanNHDMetric(get_argument_data(node))

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return (
            cursor.kind == clang.cindex.CursorKind.CXX_METHOD
            and cursor.is_definition()
        )

class MinNHDMetric(Metric):
    '''
    Represents MIN_NHD metric.
    '''

    def __init__(self, data: dict[str, dict[str, set[str]]]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, dict[str, set[str]]]): dictionary that contains set of argument types for
        each viewed method for each viewed class
        '''
        super().__init__(MIN_NHD)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MinNHDMetric):
            raise NotImplementedError
        return MinNHDMetric(merge_argument_data(self.data, other.data))

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        value = None
        if len(self.data) == 0:
            return MIN_NHD, 0
        for _, class_methods in self.data.items():
            nhd = _calculate_nhd(class_methods)
            if value is None:
                value = nhd
            else:
                value = min(value, nhd)
        if value is None:
            return MIN_NHD, 0
        return MIN_NHD, value

class MinNHDCalculator(ClangMetricCalculator):
    '''
    Calculates MIN_NHD.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MinNHDMetric({})
        return MinNHDMetric(get_argument_data(node))

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return (
            cursor.kind == clang.cindex.CursorKind.CXX_METHOD
            and cursor.is_definition()
        )

class MaxNHDMetric(Metric):
    '''
    Represents MAX_NHD metric.
    '''

    def __init__(self, data: dict[str, dict[str, set[str]]]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, dict[str, set[str]]]): dictionary that contains set of argument types for
        each viewd method for each viewed class
        '''
        super().__init__(MAX_NHD)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MaxNHDMetric):
            raise NotImplementedError
        return MaxNHDMetric(merge_argument_data(self.data, other.data))

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        value = None
        if len(self.data) == 0:
            return MAX_NHD, 0
        for _, class_methods in self.data.items():
            nhd = _calculate_nhd(class_methods)
            if value is None:
                value = nhd
            else:
                value = max(value, nhd)
        if value is None:
            return MAX_NHD, 0
        return MAX_NHD, value

class MaxNHDCalculator(ClangMetricCalculator):
    '''
    Calculates MAX_NHD.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MaxNHDMetric({})
        return MaxNHDMetric(get_argument_data(node))

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return (
            cursor.kind == clang.cindex.CursorKind.CXX_METHOD
            and cursor.is_definition()
        )
