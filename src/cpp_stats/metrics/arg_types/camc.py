'''
Module for MEAN_CAMC, MAX_CAMC and MIN_CAMC metrics.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

from cpp_stats.metrics.arg_types.base import merge_argument_data, get_argument_data

MEAN_CAMC = 'MEAN_CAMC'
MIN_CAMC = 'MIN_CAMC'
MAX_CAMC = 'MAX_CAMC'

class MeanCAMCMetric(Metric):
    '''
    Represents MEAN_CAMC metric.
    '''

    def __init__(self, data: dict[str, dict[str, set[str]]]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, dict[str, set[str]]]): dictionary that contains set of argument types for
        each viewd method for each viewed class
        '''
        super().__init__(MEAN_CAMC)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MeanCAMCMetric):
            raise NotImplementedError
        return MeanCAMCMetric(merge_argument_data(self.data, other.data))

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        summ = 0
        n = len(self.data)
        if n == 0:
            return MEAN_CAMC, 0
        for _, class_methods in self.data.items():
            all_types = set([])
            for _, argument_types in class_methods.items():
                all_types |= argument_types
            for _, argument_types in class_methods.items():
                if len(all_types) * len(class_methods) == 0:
                    continue
                summ += (len(all_types.intersection(argument_types))
                         / (len(all_types) * len(class_methods)))
        return MEAN_CAMC, summ / n

class MeanCAMCCalculator(ClangMetricCalculator):
    '''
    Calculates MEAN_CAMC.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MeanCAMCMetric({})
        return MeanCAMCMetric(get_argument_data(node))

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

class MinCAMCMetric(Metric):
    '''
    Represents MIN_CAMC metric.
    '''

    def __init__(self, data: dict[str, dict[str, set[str]]]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, dict[str, set[str]]]): dictionary that contains set of argument types for
        each viewd method for each viewed class
        '''
        super().__init__(MIN_CAMC)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MinCAMCMetric):
            raise NotImplementedError
        return MinCAMCMetric(merge_argument_data(self.data, other.data))

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        value = None
        if len(self.data) == 0:
            return MIN_CAMC, 0
        for _, class_methods in self.data.items():
            all_types = set([])
            for _, argument_types in class_methods.items():
                all_types |= argument_types
            class_value = 0
            for _, argument_types in class_methods.items():
                if len(all_types) * len(class_methods) == 0:
                    continue
                class_value += (len(all_types.intersection(argument_types))
                         / (len(all_types) * len(class_methods)))
            if value is None:
                value = class_value
            else:
                value = min(value, class_value)
        if value is None:
            return MIN_CAMC, 0
        return MIN_CAMC, value

class MinCAMCCalculator(ClangMetricCalculator):
    '''
    Calculates MIN_CAMC.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MinCAMCMetric({})
        return MinCAMCMetric(get_argument_data(node))

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

class MaxCAMCMetric(Metric):
    '''
    Represents MAX_CAMC metric.
    '''

    def __init__(self, data: dict[str, dict[str, set[str]]]):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, dict[str, set[str]]]): dictionary that contains set of argument types for
        each viewd method for each viewed class
        '''
        super().__init__(MAX_CAMC)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MaxCAMCMetric):
            raise NotImplementedError
        return MaxCAMCMetric(merge_argument_data(self.data, other.data))

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        value = None
        if len(self.data) == 0:
            return MAX_CAMC, 0
        for _, class_methods in self.data.items():
            all_types = set([])
            for _, argument_types in class_methods.items():
                all_types |= argument_types
            class_value = 0
            for _, argument_types in class_methods.items():
                if len(all_types) * len(class_methods) == 0:
                    continue
                class_value += (len(all_types.intersection(argument_types))
                         / (len(all_types) * len(class_methods)))
            if value is None:
                value = class_value
            else:
                value = max(value, class_value)
        if value is None:
            return MAX_CAMC, 0
        return MAX_CAMC, value

class MaxCAMCCalculator(ClangMetricCalculator):
    '''
    Calculates MAX_CAMC.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MaxCAMCMetric({})
        return MaxCAMCMetric(get_argument_data(node))

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
