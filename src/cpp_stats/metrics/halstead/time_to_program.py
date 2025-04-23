'''
Module for MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM and MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM = 'MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM'
MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM = 'MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM'

class MeanHalsteadTimeToProgramMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.time_required_to_program()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM,
            MeanHalsteadTimeToProgramMetric,
            data
        )

# pylint: disable=R0903
class MeanHalsteadTimeToProgramCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM.
    '''
    def __init__(self, ):
        super().__init__(
            MeanHalsteadTimeToProgramMetric
        )

class MaxHalsteadTimeToProgramMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.time_required_to_program()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM,
            MaxHalsteadTimeToProgramMetric,
            data
        )

# pylint: disable=R0903
class MaxHalsteadTimeToProgramCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM.
    '''

    def __init__(self, ):
        super().__init__(
            MaxHalsteadTimeToProgramMetric
        )
