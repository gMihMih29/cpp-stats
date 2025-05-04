'''
Module for MEAN_HALSTEAD_PROGRAM_VOCABULARY and MAX_HALSTEAD_PROGRAM_VOCABULARY metrics.
'''

from cpp_stats.metrics.halstead.base_metric import HalsteadCalculator
from cpp_stats.metrics.halstead.base_metric import MeanHalsteadMetric, MaxHalsteadMetric
from cpp_stats.metrics.halstead.base import HalsteadData

MEAN_HALSTEAD_PROGRAM_VOCABULARY = 'MEAN_HALSTEAD_PROGRAM_VOCABULARY'
MAX_HALSTEAD_PROGRAM_VOCABULARY = 'MAX_HALSTEAD_PROGRAM_VOCABULARY'

class MeanHalsteadProgramVocabularyMetric(MeanHalsteadMetric):
    '''
    Represents MEAN_HALSTEAD_PROGRAM_VOCABULARY metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.program_vocabulary()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MEAN_HALSTEAD_PROGRAM_VOCABULARY,
            MeanHalsteadProgramVocabularyMetric,
            data
        )

# pylint: disable=R0903
class MeanHalsteadProgramVocabularyCalculator(HalsteadCalculator):
    '''
    Calculates MEAN_HALSTEAD_PROGRAM_VOCABULARY.
    '''
    def __init__(self):
        super().__init__(
            MeanHalsteadProgramVocabularyMetric
        )

class MaxHalsteadProgramVocabularyMetric(MaxHalsteadMetric):
    '''
    Represents MAX_HALSTEAD_PROGRAM_VOCABULARY metric.
    '''

    @classmethod
    def value_source(cls, halstead_data: HalsteadData):
        return halstead_data.program_vocabulary()

    def __init__(self, data: dict[str, HalsteadData]):
        super().__init__(
            MAX_HALSTEAD_PROGRAM_VOCABULARY,
            MaxHalsteadProgramVocabularyMetric,
            data
        )

# pylint: disable=R0903
class MaxHalsteadProgramVocabularyCalculator(HalsteadCalculator):
    '''
    Calculates MAX_HALSTEAD_PROGRAM_VOCABULARY.
    '''

    def __init__(self):
        super().__init__(
            MaxHalsteadProgramVocabularyMetric
        )
