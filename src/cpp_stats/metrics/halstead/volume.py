'''
Module for MEAN_HALSTEAD_VOLUME and MAX_HALSTEAD_VOLUME metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_VOLUME = 'MEAN_HALSTEAD_VOLUME'
MAX_HALSTEAD_VOLUME = 'MAX_HALSTEAD_VOLUME'

class MeanHalsteadVolumeMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_VOLUME metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.volume()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_VOLUME,
            MeanHalsteadVolumeMetric,
            data
        )

class MeanHalsteadVolumeCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_VOLUME.
    '''
    def __init__(self, ):
        super().__init__(
            MeanHalsteadVolumeMetric
        )

class MaxHalsteadVolumeMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_VOLUME metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.volume()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_VOLUME,
            MaxHalsteadVolumeMetric,
            data
        )

class MaxHalsteadVolumeCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_VOLUME.
    '''

    def __init__(self, ):
        super().__init__(
            MaxHalsteadVolumeMetric
        )
