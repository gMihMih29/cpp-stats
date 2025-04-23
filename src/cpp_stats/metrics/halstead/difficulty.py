'''
Module for MEAN_HALSTEAD_DIFFICULTY and MAX_HALSTEAD_DIFFICULTY metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_DIFFICULTY = 'MEAN_HALSTEAD_DIFFICULTY'
MAX_HALSTEAD_DIFFICULTY = 'MAX_HALSTEAD_DIFFICULTY'

class MeanHalsteadDifficultyMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_DIFFICULTY metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.difficulty()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_DIFFICULTY,
            MeanHalsteadDifficultyMetric,
            data
        )

# pylint: disable=R0903
class MeanHalsteadDifficultyCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_DIFFICULTY.
    '''
    def __init__(self, ):
        super().__init__(
            MeanHalsteadDifficultyMetric
        )

class MaxHalsteadDifficultyMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_DIFFICULTY metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.difficulty()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_DIFFICULTY,
            MaxHalsteadDifficultyMetric,
            data
        )

# pylint: disable=R0903
class MaxHalsteadDifficultyCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_DIFFICULTY.
    '''

    def __init__(self, ):
        super().__init__(
            MaxHalsteadDifficultyMetric
        )
