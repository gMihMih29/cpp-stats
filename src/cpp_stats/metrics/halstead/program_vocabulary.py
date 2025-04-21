'''
Module for MEAN_HALSTEAD_PROGRAM_VOCABULARY and MAX_HALSTEAD_PROGRAM_VOCABULARY metrics.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator
from cpp_stats.metrics.halstead import base

MEAN_HALSTEAD_PROGRAM_VOCABULARY = 'MEAN_HALSTEAD_PROGRAM_VOCABULARY'
MAX_HALSTEAD_PROGRAM_VOCABULARY = 'MAX_HALSTEAD_PROGRAM_VOCABULARY'

class MeanHalsteadProgramVocabularyMetric(Metric):
    def __init__(self, data: dict[str, base.HalsteadData]):
        super().__init__(MEAN_HALSTEAD_PROGRAM_VOCABULARY)
        self._data = data

    def __add__(self, other):
        if not isinstance(other, MeanHalsteadProgramVocabularyMetric):
            raise NotImplementedError
        return MeanHalsteadProgramVocabularyMetric(base.merge_data(self._data, other._data))

    def get(self) -> tuple[str, float]:
        sum_vocabulary = 0
        cnt_classes = len(self._data)
        for file_name, hastead_data in self._data.items():
            # hastead_data += base.find_remaining_operators(file_name)
            sum_vocabulary += hastead_data.program_vocabulary()
        value = 0
        if cnt_classes != 0:
            value = sum_vocabulary / cnt_classes
        return MEAN_HALSTEAD_PROGRAM_VOCABULARY, value

class MeanHalsteadProgramVocabularyCalculator(ClangMetricCalculator):
    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        return MeanHalsteadProgramVocabularyMetric({
            node.location.file.name: base.create_data(node)
        })

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        return True
