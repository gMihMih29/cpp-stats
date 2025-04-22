'''
Module for MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS and MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS = 'MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS'
MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS = 'MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS'

class MeanHalsteadDeliveredBugsMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.delivered_bugs()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS,
            MeanHalsteadDeliveredBugsMetric,
            data
        )

class MeanHalsteadDeliveredBugsCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS.
    '''
    def __init__(self, ):
        super().__init__(
            MeanHalsteadDeliveredBugsMetric
        )

class MaxHalsteadDeliveredBugsMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.delivered_bugs()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS,
            MaxHalsteadDeliveredBugsMetric,
            data
        )

class MaxHalsteadDeliveredBugsCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS.
    '''

    def __init__(self, ):
        super().__init__(
            MaxHalsteadDeliveredBugsMetric
        )
