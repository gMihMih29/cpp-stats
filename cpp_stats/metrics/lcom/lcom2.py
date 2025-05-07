'''
Module for MEAN_LCOM2 and MAX_LCOM2 metrics.
'''

from cpp_stats.metrics.lcom.base import LCOMClassData
from cpp_stats.metrics.lcom.base_metric import MaxLCOMMetric, MeanLCOMMetric, LCOMCalculator

MEAN_LCOM2 = 'MEAN_LCOM2'
MAX_LCOM2 = 'MAX_LCOM2'

def _get_lcom2(data: LCOMClassData) -> float:
    summ = 0
    if len(data.fields) == 0 or len(data.method_data) == 0:
        return 0
    for field in data.fields:
        for _, method_data in data.method_data.items():
            if field not in method_data.used_fields:
                summ += 1
    return summ / (len(data.fields) * len(data.method_data))

class MeanLCOM2Metric(MeanLCOMMetric):
    '''
    Represents MEAN_LCOM2 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom2(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MEAN_LCOM2,
            MeanLCOM2Metric,
            data
        )

# pylint: disable=R0903
class MeanLCOM2Calculator(LCOMCalculator):
    '''
    Calculates MEAN_LCOM2.
    '''

    def __init__(self):
        super().__init__(
            MeanLCOM2Metric
        )

class MaxLCOM2Metric(MaxLCOMMetric):
    '''
    Represents MAX_LCOM2 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom2(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MAX_LCOM2,
            MaxLCOM2Metric,
            data
        )

# pylint: disable=R0903
class MaxLCOM2Calculator(LCOMCalculator):
    '''
    Calculates MAX_LCOM2.
    '''

    def __init__(self):
        super().__init__(
            MaxLCOM2Metric
        )
