'''
Module for MEAN_TCC and MIN_TCC metrics.
'''

from cpp_stats.metrics.lcom.base import LCOMClassData
from cpp_stats.metrics.lcom.base_metric import MinLCOMMetric, MeanLCOMMetric, LCOMCalculator
from cpp_stats.metrics.lcom.tcc_lcc.base import calculate_connections

MEAN_TCC = 'MEAN_TCC'
MIN_TCC = 'MIN_TCC'

def _get_tcc(data: LCOMClassData) -> float:
    '''
    Returns TCC value for given class data.
    '''
    np, ndc, _ = calculate_connections(data)
    if np == 0:
        return 0
    return ndc / np

class MeanTCCMetric(MeanLCOMMetric):
    '''
    Represents MEAN_TCC metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_tcc(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MEAN_TCC,
            MeanTCCMetric,
            data
        )

# pylint: disable=R0903
class MeanTCCCalculator(LCOMCalculator):
    '''
    Calculates MEAN_TCC.
    '''

    def __init__(self):
        super().__init__(
            MeanTCCMetric
        )

class MinTCCMetric(MinLCOMMetric):
    '''
    Represents MIN_TCC metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_tcc(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MIN_TCC,
            MinTCCMetric,
            data
        )

# pylint: disable=R0903
class MinTCCCalculator(LCOMCalculator):
    '''
    Calculates MIN_TCC.
    '''

    def __init__(self):
        super().__init__(
            MinTCCMetric
        )
