'''
Module for base lcom metrics.
'''
import math

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator
from cpp_stats.metrics.lcom import base

class MeanLCOMMetric(Metric):
    '''
    Represents abstract mean lcom metric.
    '''

    def __init__(self, name, true_type, data: dict[str, base.LCOMClassData]):
        super().__init__(name)
        self._type = true_type
        self.data = data

    def __add__(self, other):
        if not isinstance(other, self._type):
            raise NotImplementedError
        return self._type(
            base.merge_class_lcom_data(self.data, other.data)
        )

    def get(self) -> tuple[str, float]:
        summ = 0
        cnt = len(self.data)
        for _, lcom_data in self.data.items():
            if math.isnan(self._type.value_source(lcom_data).real):
                continue
            summ += self._type.value_source(lcom_data).real
        value = 0
        if cnt != 0:
            value = summ / cnt
        return self.name(), value

    @classmethod
    def value_source(cls, lcom_data: base.LCOMClassData) -> float:
        '''
        Returns value used by MeanLCOMMetric during calculations
        '''

class MaxLCOMMetric(Metric):
    '''
    Represents abstract max lcom metric.
    '''

    def __init__(self, name, true_type, data: dict[str, base.LCOMClassData]):
        super().__init__(name)
        self._type = true_type
        self.data = data

    def __add__(self, other):
        if not isinstance(other, self._type):
            raise NotImplementedError
        return self._type(
            base.merge_class_lcom_data(self.data, other.data)
        )

    def get(self) -> tuple[str, float]:
        result = 0.0
        for _, lcom_data in self.data.items():
            if math.isnan(self._type.value_source(lcom_data).real):
                continue
            result = max(result, self._type.value_source(lcom_data).real)
        return self.name(), result

    @classmethod
    def value_source(cls, lcom_data: base.LCOMClassData) -> float:
        '''
        Returns value used by MeanLCOMMetric during calculations
        '''

class LCOMCalculator(ClangMetricCalculator):
    '''
    Calculates abstract lcom metric.
    '''

    def __init__(self, metric_type):
        super().__init__()
        self._metric_type = metric_type

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if not self.validate_cursor(node):
            return self._metric_type({})
        data = base.get_lcom_data(node)
        return self._metric_type({
            data.class_name: data
        })

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        return (
            cursor.kind in [
                clang.cindex.CursorKind.CXX_METHOD,
                clang.cindex.CursorKind.FIELD_DECL
            ]
            and cursor.is_definition()
        )
