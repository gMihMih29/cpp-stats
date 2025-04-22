'''
Module for base halstead metrics.
'''

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
        self._data = data

    def __add__(self, other):
        if not isinstance(other, self._type):
            raise NotImplementedError
        return self._type(
            base.merge_data(self._data, other._data)
        )

    def get(self) -> tuple[str, float]:
        sum_vocabulary = 0
        cnt_files = len(self._data)
        for _, halstead_data in self._data.items():
            sum_vocabulary += self._type.value_source(halstead_data)
        value = 0
        if cnt_files != 0:
            value = sum_vocabulary / cnt_files
        return self.name(), value

    @classmethod
    def value_source(cls, halstead_data: base.HalsteadData):
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
        self._data = data

    def __add__(self, other):
        if not isinstance(other, self._type):
            raise NotImplementedError
        return self._type(
            base.merge_data(self._data, other._data)
        )

    def get(self) -> tuple[str, float]:
        result = 0
        for _, halstead_data in self._data.items():
            result = max(result, self._type.value_source(halstead_data))
        return self.name(), result

    @classmethod
    def value_source(cls, halstead_data: base.HalsteadData):
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
        return self._metric_type(
            {
                node.location.file.name: base.create_data(node)
            }
        )

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        return True
