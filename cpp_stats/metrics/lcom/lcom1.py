'''
Module for MEAN_LCOM1 and MAX_LCOM1 metrics.
'''

from cpp_stats.metrics.lcom.base import LCOMClassData
from cpp_stats.metrics.lcom.base_metric import MaxLCOMMetric, MeanLCOMMetric, LCOMCalculator

MEAN_LCOM1 = 'MEAN_LCOM1'
MAX_LCOM1 = 'MAX_LCOM1'

def _get_lcom1(data: LCOMClassData) -> float:
    p = 0
    q = 0
    for method_name_lhv, method_value_lhv in data.method_data.items():
        for method_name_rhv, method_value_rhv in data.method_data.items():
            if method_name_lhv == method_name_rhv:
                continue
            if len(method_value_lhv.used_fields.intersection(method_value_rhv.used_fields)) != 0:
                q += 1
            else:
                p += 1
    q /= 2
    p /= 2
    return max(0, p - q)

class MeanLCOM1Metric(MeanLCOMMetric):
    '''
    Represents MEAN_LCOM1 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom1(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MEAN_LCOM1,
            MeanLCOM1Metric,
            data
        )

# pylint: disable=R0903
class MeanLCOM1Calculator(LCOMCalculator):
    '''
    Calculates MEAN_LCOM1.
    '''

    def __init__(self):
        super().__init__(
            MeanLCOM1Metric
        )

class MaxLCOM1Metric(MaxLCOMMetric):
    '''
    Represents MAX_LCOM1 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom1(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MAX_LCOM1,
            MaxLCOM1Metric,
            data
        )

# pylint: disable=R0903
class MaxLCOM1Calculator(LCOMCalculator):
    '''
    Calculates MAX_LCOM1.
    '''

    def __init__(self):
        super().__init__(
            MaxLCOM1Metric
        )
