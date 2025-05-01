'''
Module for base halstead metrics.
'''
import math

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator
from cpp_stats.metrics.halstead import base

class MeanHalsteadMetric(Metric):
    '''
    Represents abstract mean halstead metric.
    '''

    def __init__(self, name, true_type, data: dict[str, base.HalsteadData]):
        super().__init__(name)
        self._type = true_type
        self.data = data

    def __add__(self, other):
        if not isinstance(other, self._type):
            raise NotImplementedError
        return self._type(
            base.merge_data(self.data, other.data)
        )

    def get(self) -> tuple[str, float]:
        sum_vocabulary = 0
        cnt_files = len(self.data)
        for _, halstead_data in self.data.items():
            if math.isnan(self._type.value_source(halstead_data).real):
                continue
            sum_vocabulary += self._type.value_source(halstead_data).real
        value = 0
        if cnt_files != 0:
            value = sum_vocabulary / cnt_files
        return self.name(), value

    @classmethod
    def value_source(cls, halstead_data: base.HalsteadData) -> float:
        '''
        Returns value used by MeanHalsteadMetric during calculations
        '''

class MaxHalsteadMetric(Metric):
    '''
    Represents abstract max halstead metric.
    '''

    def __init__(self, name, true_type, data: dict[str, base.HalsteadData]):
        super().__init__(name)
        self._type = true_type
        self.data = data

    def __add__(self, other):
        if not isinstance(other, self._type):
            raise NotImplementedError
        return self._type(
            base.merge_data(self.data, other.data)
        )

    def get(self) -> tuple[str, float]:
        result = 0.0
        for _, halstead_data in self.data.items():
            if math.isnan(self._type.value_source(halstead_data).real):
                continue
            print(self._type.value_source(halstead_data).real)
            result = max(result, self._type.value_source(halstead_data).real)
        return self.name(), result

    @classmethod
    def value_source(cls, halstead_data: base.HalsteadData) -> float:
        '''
        Returns value used by MeanHalsteadMetric during calculations
        '''

class HalsteadCalculator(ClangMetricCalculator):
    '''
    Calculates abstract halstead metric.
    '''

    def __init__(self, metric_type):
        super().__init__()
        self._metric_type = metric_type

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if node.kind.is_translation_unit():
            return self._metric_type(
            {
                node.spelling: base.create_data(node)
            }
        )
        return self._metric_type(
            {
                node.location.file.name: base.create_data(node)
            }
        )

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        return True
