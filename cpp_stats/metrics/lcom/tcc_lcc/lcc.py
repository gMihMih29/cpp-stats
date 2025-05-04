'''
Module for MEAN_LCC and MIN_LCC metrics.
'''

from cpp_stats.metrics.lcom.base import LCOMClassData
from cpp_stats.metrics.lcom.base_metric import MinLCOMMetric, MeanLCOMMetric, LCOMCalculator
from cpp_stats.metrics.lcom.tcc_lcc.base import calculate_connections

MEAN_LCC = 'MEAN_LCC'
MIN_LCC = 'MIN_LCC'

def _get_lcc(data: LCOMClassData) -> float:
    '''
    Returns LCC value for given class data.
    '''
    np, ndc, nic = calculate_connections(data)
    if np == 0:
        return 0
    return (ndc + nic) / np

class MeanLCCMetric(MeanLCOMMetric):
    '''
    Represents MEAN_LCC metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcc(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MEAN_LCC,
            MeanLCCMetric,
            data
        )

# pylint: disable=R0903
class MeanLCCCalculator(LCOMCalculator):
    '''
    Calculates MEAN_LCC.
    '''

    def __init__(self):
        super().__init__(
            MeanLCCMetric
        )

class MinLCCMetric(MinLCOMMetric):
    '''
    Represents MIN_LCC metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcc(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MIN_LCC,
            MinLCCMetric,
            data
        )

# pylint: disable=R0903
class MinLCCCalculator(LCOMCalculator):
    '''
    Calculates MIN_LCC.
    '''

    def __init__(self):
        super().__init__(
            MinLCCMetric
        )
