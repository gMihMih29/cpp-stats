'''
Module for MEAN_HALSTEAD_PROGRAM_LENGTH and MAX_HALSTEAD_PROGRAM_LENGTH metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_PROGRAM_LENGTH = 'MEAN_HALSTEAD_PROGRAM_LENGTH'
MAX_HALSTEAD_PROGRAM_LENGTH = 'MAX_HALSTEAD_PROGRAM_LENGTH'

class MeanHalsteadProgramLengthMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_PROGRAM_LENGTH metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.program_length()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_PROGRAM_LENGTH,
            MeanHalsteadProgramLengthMetric,
            data
        )

class MeanHalsteadProgramLengthCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_PROGRAM_LENGTH.
    '''
    def __init__(self, ):
        super().__init__(
            MeanHalsteadProgramLengthMetric
        )

class MaxHalsteadProgramLengthMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_PROGRAM_LENGTH metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.program_length()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_PROGRAM_LENGTH,
            MaxHalsteadProgramLengthMetric,
            data
        )

class MaxHalsteadProgramLengthCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_PROGRAM_LENGTH.
    '''

    def __init__(self, ):
        super().__init__(
            MaxHalsteadProgramLengthMetric
        )
