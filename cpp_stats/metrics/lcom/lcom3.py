'''
Module for MEAN_LCOM3 and MAX_LCOM3 metrics.
'''

from cpp_stats.metrics.lcom.base import LCOMClassData
from cpp_stats.metrics.lcom.base_metric import MaxLCOMMetric, MeanLCOMMetric, LCOMCalculator
from cpp_stats.metrics.lcom.lcom2 import _get_lcom2

MEAN_LCOM3 = 'MEAN_LCOM3'
MAX_LCOM3 = 'MAX_LCOM3'

def _get_lcom3(data: LCOMClassData) -> float:
    if len(data.method_data) <= 1:
        return 0
    m = len(data.method_data)
    return (m - (1 - _get_lcom2(data))) / (m - 1)

class MeanLCOM3Metric(MeanLCOMMetric):
    '''
    Represents MEAN_LCOM3 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom3(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MEAN_LCOM3,
            MeanLCOM3Metric,
            data
        )

# pylint: disable=R0903
class MeanLCOM3Calculator(LCOMCalculator):
    '''
    Calculates MEAN_LCOM3.
    '''

    def __init__(self):
        super().__init__(
            MeanLCOM3Metric
        )

class MaxLCOM3Metric(MaxLCOMMetric):
    '''
    Represents MAX_LCOM3 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom3(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MAX_LCOM3,
            MaxLCOM3Metric,
            data
        )

# pylint: disable=R0903
class MaxLCOM3Calculator(LCOMCalculator):
    '''
    Calculates MAX_LCOM3.
    '''

    def __init__(self):
        super().__init__(
            MaxLCOM3Metric
        )
