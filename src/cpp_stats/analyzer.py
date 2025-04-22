'''
Main class for calculating metrics.
'''

from pathlib import Path
import clang.cindex

from cpp_stats.metrics.lines_of_code import LinesOfCodeCalculator
from cpp_stats.metrics.number_of_classes import NumberOfClassesCalculator
from cpp_stats.metrics.length_of_method import MeanLengthOfMethodsCalculator
from cpp_stats.metrics.length_of_method import MaxLengthOfMethodsCalculator
from cpp_stats.metrics.number_of_methods import MeanNumberOfMethodsCalculator
from cpp_stats.metrics.number_of_methods import MaxNumberOfMethodsCalculator
from cpp_stats.metrics.cognitive_complexity import MeanCognitiveComplexityCalculator
from cpp_stats.metrics.cognitive_complexity import MaxCognitiveComplexityCalculator
from cpp_stats.metrics.cyclomatic_complexity import MeanCyclomaticComplexityCalculator
from cpp_stats.metrics.cyclomatic_complexity import MaxCyclomaticComplexityCalculator
from cpp_stats.metrics.halstead.program_vocabulary import MeanHalsteadProgramVocabularyCalculator
from cpp_stats.metrics.halstead.program_vocabulary import MaxHalsteadProgramVocabularyCalculator
from cpp_stats.metrics.halstead.program_length import MeanHalsteadProgramLengthCalculator
from cpp_stats.metrics.halstead.program_length import MaxHalsteadProgramLengthCalculator
from cpp_stats.metrics.halstead.estimated_program_length import MeanHalsteadEstimatedProgramLengthCalculator
from cpp_stats.metrics.halstead.estimated_program_length import MaxHalsteadEstimatedProgramLengthCalculator
from cpp_stats.metrics.halstead.volume import MeanHalsteadVolumeCalculator
from cpp_stats.metrics.halstead.volume import MaxHalsteadVolumeCalculator
from cpp_stats.metrics.halstead.difficulty import MeanHalsteadDifficultyCalculator
from cpp_stats.metrics.halstead.difficulty import MaxHalsteadDifficultyCalculator
from cpp_stats.metrics.halstead.effort import MeanHalsteadEffortCalculator
from cpp_stats.metrics.halstead.effort import MaxHalsteadEffortCalculator
from cpp_stats.metrics.halstead.time_to_program import MeanHalsteadTimeToProgramCalculator
from cpp_stats.metrics.halstead.time_to_program import MaxHalsteadTimeToProgramCalculator
from cpp_stats.metrics.halstead.delivered_bugs import MeanHalsteadDeliveredBugsCalculator
from cpp_stats.metrics.halstead.delivered_bugs import MaxHalsteadDeliveredBugsCalculator
from cpp_stats.metrics.metric_calculator import Metric
from cpp_stats.ast.ast_tree import analyze_ast

# pylint: disable=R0903
class CodeAnalyzer:
    '''
    Provides calculated metrics.
    '''

    def __init__(self, repo_path: str, c_cxx_files: list[Path], clang_path: str = None):
        self._files = c_cxx_files
        self._ast_tree = None
        self._basic_calculators = {
            'LINES_OF_CODE' : LinesOfCodeCalculator(),
        }
        self._clang_calculators = {
            'NUMBER_OF_CLASSES' : NumberOfClassesCalculator(),
            'MEAN_LENGTH_OF_METHODS': MeanLengthOfMethodsCalculator(),
            'MAX_LENGTH_OF_METHODS': MaxLengthOfMethodsCalculator(),
            'MEAN_NUMBER_OF_METHODS_PER_CLASS': MeanNumberOfMethodsCalculator(),
            'MAX_NUMBER_OF_METHODS_PER_CLASS': MaxNumberOfMethodsCalculator(),
            'MEAN_COGNITIVE_COMPLEXITY': MeanCognitiveComplexityCalculator(),
            'MAX_COGNITIVE_COMPLEXITY': MaxCognitiveComplexityCalculator(),
            'MEAN_CYCLOMATIC_COMPLEXITY': MeanCyclomaticComplexityCalculator(),
            'MAX_CYCLOMATIC_COMPLEXITY': MaxCyclomaticComplexityCalculator(),
            # 'MEAN_HALSTEAD_PROGRAM_VOCABULARY': MeanHalsteadProgramVocabularyCalculator(),
            'MAX_HALSTEAD_PROGRAM_VOCABULARY': MaxHalsteadProgramVocabularyCalculator(),
            # 'MEAN_HALSTEAD_PROGRAM_LENGTH': MeanHalsteadProgramLengthCalculator(),
            # 'MAX_HALSTEAD_PROGRAM_LENGTH': MaxHalsteadProgramLengthCalculator(),
            # 'MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH': MeanHalsteadEstimatedProgramLengthCalculator(),
            # 'MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH': MaxHalsteadEstimatedProgramLengthCalculator(),
            # 'MEAN_HALSTEAD_VOLUME': MeanHalsteadVolumeCalculator(),
            # 'MAX_HALSTEAD_VOLUME': MaxHalsteadVolumeCalculator(),
            # 'MEAN_HALSTEAD_DIFFICULTY': MeanHalsteadDifficultyCalculator(),
            # 'MAX_HALSTEAD_DIFFICULTY': MaxHalsteadDifficultyCalculator(),
            # 'MEAN_HALSTEAD_EFFORT': MeanHalsteadEffortCalculator(),
            # 'MAX_HALSTEAD_EFFORT': MaxHalsteadEffortCalculator(),
            # 'MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM': MeanHalsteadTimeToProgramCalculator(),
            # 'MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM': MaxHalsteadTimeToProgramCalculator(),
            # 'MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS': MeanHalsteadDeliveredBugsCalculator(),
            # 'MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS': MaxHalsteadDeliveredBugsCalculator(),
        }
        self._cache = {
            'LINES_OF_CODE' : None,
            'NUMBER_OF_CLASSES' : None,
        }
        self._clang_cache = None
        self._use_clang = False
        if clang_path is not None:
            self._use_clang = True
            clang.cindex.Config.set_library_file(clang_path)
            index = clang.cindex.Index.create()
            self._clang_cache = analyze_ast(index, repo_path, c_cxx_files, self._clang_calculators)

    def metric(self, metric_name: str) -> Metric | None:
        '''
        Returns calculated metric by name.
        
        Parameters:
        metric_name (str): Metric name.
        '''
        if self._cache.get(metric_name, None) is not None:
            return self._cache[metric_name]
        if self._use_clang and self._clang_cache.get(metric_name, None) is not None:
            return self._clang_cache[metric_name]
        if self._basic_calculators.get(metric_name, None) is not None:
            self._cache[metric_name] = self._basic_calculators[metric_name](self._files)
        return self._cache.get(metric_name, None)
