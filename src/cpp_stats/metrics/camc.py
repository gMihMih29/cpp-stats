'''
Module for MEAN_CYCLOMATIC_COMPLEXITY and MAX_CYCLOMATIC_COMPLEXITY metrics.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

from cpp_stats.metrics.utils import mangle_cursor_name

MEAN_CAMC = 'MEAN_CAMC'
MIN_CAMC = 'MIN_CAMC'
MAX_CAMC = 'MAX_CAMC'

def _merge_class_data(lhv: dict[str, set[str]], rhv: dict[str, set[str]]):
    result = {}
    for key, item in lhv.items():
        result[key] = item
    for key, item in rhv.items():
        if result.get(key, None) is None:
            result[key] = item
        else:
            result[key] |= item
    return result

def _merge_data(lhv: dict[str, dict[str, set[str]]], rhv: dict[str, dict[str, set[str]]]):
    result = {}
    for key, item in lhv.items():
        result[key] = item
    for key, item in rhv.items():
        if result.get(key, None) is None:
            result[key] = item
        else:
            result[key] = _merge_class_data(result[key], item)
    return result

def _get_set_of_argument_types(method: clang.cindex.Cursor) -> set[str]:
    result = set([])
    for child in method.get_children():
        if child.kind == clang.cindex.CursorKind.COMPOUND_STMT:
            break
        if child.kind == clang.cindex.CursorKind.PARM_DECL:
            result |= set([child.type.spelling])
    return result

def _get_data(method: clang.cindex.Cursor):
    return {
        mangle_cursor_name(method.semantic_parent): {
            method.mangled_name: _get_set_of_argument_types(method)
        }
    }

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
        return MeanCAMCMetric(_merge_data(self.data, other.data))

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
        return MeanCAMCMetric(_get_data(node))

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
        return MinCAMCMetric(_merge_data(self.data, other.data))

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
            return MIN_CAMC, value
        return MIN_CAMC, value

class MinCAMCCalculator(ClangMetricCalculator):
    '''
    Calculates MIN_CAMC.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MinCAMCMetric({})
        return MinCAMCMetric(_get_data(node))

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
        return MaxCAMCMetric(_merge_data(self.data, other.data))

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
                value = max(value, class_value)
        if value is None:
            return MIN_CAMC, value
        return MIN_CAMC, value

class MaxCAMCCalculator(ClangMetricCalculator):
    '''
    Calculates MAX_CAMC.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return MaxCAMCMetric({})
        return MaxCAMCMetric(_get_data(node))

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
