'''
Module for MEAN_HALSTEAD_EFFORT, SUM_HALSTEAD_EFFORT and MAX_HALSTEAD_EFFORT metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base_metric import SumHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_EFFORT = 'MEAN_HALSTEAD_EFFORT'
MAX_HALSTEAD_EFFORT = 'MAX_HALSTEAD_EFFORT'
SUM_HALSTEAD_EFFORT = 'SUM_HALSTEAD_EFFORT'

class MeanHalsteadEffortMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_EFFORT metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.effort()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_EFFORT,
            MeanHalsteadEffortMetric,
            data
        )

# pylint: disable=R0903
class MeanHalsteadEffortCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_EFFORT.
    '''
    def __init__(self, ):
        super().__init__(
            MeanHalsteadEffortMetric
        )

class MaxHalsteadEffortMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_EFFORT metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.effort()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_EFFORT,
            MaxHalsteadEffortMetric,
            data
        )

# pylint: disable=R0903
class MaxHalsteadEffortCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_EFFORT.
    '''

    def __init__(self, ):
        super().__init__(
            MaxHalsteadEffortMetric
        )

class SumHalsteadEffortMetric(SumHalsteadMetric):
    '''
    Represents SUM_HALSTEAD_EFFORT metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.effort()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            SUM_HALSTEAD_EFFORT,
            SumHalsteadEffortMetric,
            data
        )

# pylint: disable=R0903
class SumHalsteadEffortCalculator(HalsteadCalculator):
    '''
    Calculates SUM_HALSTEAD_EFFORT.
    '''

    def __init__(self, ):
        super().__init__(
            SumHalsteadEffortMetric
        )
