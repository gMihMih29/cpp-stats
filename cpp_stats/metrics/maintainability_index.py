'''
Module for MAINTAINABILITY_INDEX metric.
'''
import math

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator
from cpp_stats.metrics.halstead.volume import MeanHalsteadVolumeCalculator
from cpp_stats.metrics.halstead.volume import MeanHalsteadVolumeMetric
from cpp_stats.metrics.cyclomatic_complexity import MeanCyclomaticComplexityCalculator
from cpp_stats.metrics.cyclomatic_complexity import MeanCyclomaticComplexityMetric

MEAN_MAINTAINABILITY_INDEX = 'MEAN_MAINTAINABILITY_INDEX'
MIN_MAINTAINABILITY_INDEX = 'MIN_MAINTAINABILITY_INDEX'

def _merge_data(lhv: dict[str, (int, MeanHalsteadVolumeMetric, MeanCyclomaticComplexityMetric)],
                rhv: dict[str, (int, MeanHalsteadVolumeMetric, MeanCyclomaticComplexityMetric)]):
    '''
    Merges data for maintainability index according to file names.
    '''
    new_data = {}
    for file_name, item in lhv.items():
        new_data[file_name] = item
    for file_name, item in rhv.items():
        if new_data.get(file_name, None) is None:
            new_data[file_name] = item
        else:
            lhv_loc, lhv_volume, lhv_cycl = new_data[file_name]
            rhv_loc, rhv_volume, rhv_cycl = item
            new_data[file_name] = (
                lhv_loc + rhv_loc,
                lhv_volume + rhv_volume,
                lhv_cycl + rhv_cycl
            )
    return new_data

class MeanMaintainabilityIndexMetric(Metric):
    '''
    Represents MEAN_MAINTAINABILITY_INDEX metric.
    '''

    def __init__(self,
                 data: dict[str, (int, MeanHalsteadVolumeMetric, MeanCyclomaticComplexityMetric)]
                 ):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, (int, MeanHalsteadVolumeMetric, MeanCyclomaticComplexityMetric)]):
        dictionary that stores metrics for each viewed file.
        '''
        super().__init__(MEAN_MAINTAINABILITY_INDEX)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MeanMaintainabilityIndexMetric):
            raise NotImplementedError
        return MeanMaintainabilityIndexMetric(
            _merge_data(self.data, other.data)
        )

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        if len(self.data) == 0:
            return MEAN_MAINTAINABILITY_INDEX, 0
        summ = 0
        n = 0
        for file_name, item in self.data.items():
            loc, volume, cyclomatic = item
            if volume.data[file_name].volume() == 0 or loc == 0:
                continue
            value = max(0,
                        171
                        - 5.2 * math.log(volume.data[file_name].volume().real)
                        - 0.23 * cyclomatic.sum_value - 16.2 * math.log(loc))
            summ += value
            n += 1
        if n == 0:
            return MEAN_MAINTAINABILITY_INDEX, 0
        return MEAN_MAINTAINABILITY_INDEX, summ / n

class MeanMaintainabilityIndexCalculator(ClangMetricCalculator):
    '''
    Calculates MEAN_MAINTAINABILITY_INDEX.
    '''

    def __init__(self):
        super().__init__()
        self.__volume_calc = MeanHalsteadVolumeCalculator()
        self.__cyclomatic_calc = MeanCyclomaticComplexityCalculator()

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        loc = 0
        if node.kind == clang.cindex.CursorKind.TRANSLATION_UNIT:
            loc = node.extent.end.line - node.extent.start.line + 1
        if node.kind.is_translation_unit():
            location = node.spelling
        else:
            location = node.location.file.name
        return MeanMaintainabilityIndexMetric({
            location: (
                    loc,
                    self.__volume_calc(node),
                    self.__cyclomatic_calc(node)
                )
        })

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return True

class MinMaintainabilityIndexMetric(Metric):
    '''
    Represents MIN_MAINTAINABILITY_INDEX metric.
    '''

    def __init__(self,
                 data: dict[str, (int, MeanHalsteadVolumeMetric, MeanCyclomaticComplexityMetric)]
                 ):
        '''
        Initializes metric.
        
        Parameters:
        data (dict[str, (int, MeanHalsteadVolumeMetric, MeanCyclomaticComplexityMetric)]):
        dictionary that stores metrics for each viewed file.
        '''
        super().__init__(MIN_MAINTAINABILITY_INDEX)
        self.data = data

    def __add__(self, other):
        if not isinstance(other, MinMaintainabilityIndexMetric):
            raise NotImplementedError
        return MinMaintainabilityIndexMetric(
            _merge_data(self.data, other.data)
        )

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        if len(self.data) == 0:
            return MIN_MAINTAINABILITY_INDEX, 0
        result = 1e5
        for file_name, item in self.data.items():
            loc, volume, cyclomatic = item
            if volume.data[file_name].volume() == 0 or loc == 0:
                continue
            value = max(0,
                        171
                        - 5.2 * math.log(volume.data[file_name].volume().real)
                        - 0.23 * cyclomatic.sum_value - 16.2 * math.log(loc))
            result = min(result, value)
        return MIN_MAINTAINABILITY_INDEX, result

class MinMaintainabilityIndexCalculator(ClangMetricCalculator):
    '''
    Calculates MIN_MAINTAINABILITY_INDEX.
    '''

    def __init__(self):
        super().__init__()
        self.__volume_calc = MeanHalsteadVolumeCalculator()
        self.__cyclomatic_calc = MeanCyclomaticComplexityCalculator()

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        loc = 0
        if node.kind == clang.cindex.CursorKind.TRANSLATION_UNIT:
            loc = node.extent.end.line - node.extent.start.line + 1
        if node.kind.is_translation_unit():
            location = node.spelling
        else:
            location = node.location.file.name
        return MinMaintainabilityIndexMetric({
            location: (
                    loc,
                    self.__volume_calc(node),
                    self.__cyclomatic_calc(node)
                )
        })

    def validate_cursor(self, cursor: clang.cindex.Cursor) -> bool:
        '''
        Validates that given cursor can be used for calculation 
        by this calculator in `__call__`.

        Returns:
        bool: can cursor be used for calculation or not.
        '''
        return True
