'''
Module for MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH and MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH = 'MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH'
MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH = 'MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH'

class MeanHalsteadEstimatedProgramLengthMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.estimated_length()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH,
            MeanHalsteadEstimatedProgramLengthMetric,
            data
        )

# pylint: disable=R0903
class MeanHalsteadEstimatedProgramLengthCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH.
    '''
    def __init__(self, ):
        super().__init__(
            MeanHalsteadEstimatedProgramLengthMetric
        )

class MaxHalsteadEstimatedProgramLengthMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.estimated_length()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH,
            MaxHalsteadEstimatedProgramLengthMetric,
            data
        )

# pylint: disable=R0903
class MaxHalsteadEstimatedProgramLengthCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH.
    '''

    def __init__(self, ):
        super().__init__(
            MaxHalsteadEstimatedProgramLengthMetric
        )
