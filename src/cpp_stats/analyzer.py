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
from cpp_stats.metrics.halstead import program_vocabulary, program_length, estimated_program_length
from cpp_stats.metrics.halstead import volume, difficulty, effort, time_to_program, delivered_bugs
from cpp_stats.metrics.maintainability_index import MeanMaintainabilityIndexCalculator
from cpp_stats.metrics.maintainability_index import MinMaintainabilityIndexCalculator
from cpp_stats.metrics.arg_types.camc import MinCAMCCalculator
from cpp_stats.metrics.arg_types.camc import MeanCAMCCalculator
from cpp_stats.metrics.arg_types.camc import MaxCAMCCalculator
from cpp_stats.metrics.arg_types.nhd import MinNHDCalculator
from cpp_stats.metrics.arg_types.nhd import MeanNHDCalculator
from cpp_stats.metrics.arg_types.nhd import MaxNHDCalculator
from cpp_stats.metrics.lcom.lcom1 import MeanLCOM1Calculator, MaxLCOM1Calculator
from cpp_stats.metrics.lcom.lcom2 import MeanLCOM2Calculator, MaxLCOM2Calculator
from cpp_stats.metrics.lcom.lcom3 import MeanLCOM3Calculator, MaxLCOM3Calculator
from cpp_stats.metrics.lcom.lcom4 import MeanLCOM4Calculator, MaxLCOM4Calculator
from cpp_stats.metrics.lcom.tcc_lcc.lcc import MeanLCCCalculator, MinLCCCalculator
from cpp_stats.metrics.lcom.tcc_lcc.tcc import MeanTCCCalculator, MinTCCCalculator
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
            'MEAN_HALSTEAD_PROGRAM_VOCABULARY':
                program_vocabulary.MeanHalsteadProgramVocabularyCalculator(),
            'MAX_HALSTEAD_PROGRAM_VOCABULARY':
                program_vocabulary.MaxHalsteadProgramVocabularyCalculator(),
            'MEAN_HALSTEAD_PROGRAM_LENGTH':
                program_length.MeanHalsteadProgramLengthCalculator(),
            'MAX_HALSTEAD_PROGRAM_LENGTH':
                program_length.MaxHalsteadProgramLengthCalculator(),
            'MEAN_HALSTEAD_ESTIMATED_PROGRAM_LENGTH':
                estimated_program_length.MeanHalsteadEstimatedProgramLengthCalculator(),
            'MAX_HALSTEAD_ESTIMATED_PROGRAM_LENGTH':
                estimated_program_length.MaxHalsteadEstimatedProgramLengthCalculator(),
            'MEAN_HALSTEAD_VOLUME':
                volume.MeanHalsteadVolumeCalculator(),
            'MAX_HALSTEAD_VOLUME':
                volume.MaxHalsteadVolumeCalculator(),
            'MEAN_HALSTEAD_DIFFICULTY':
                difficulty.MeanHalsteadDifficultyCalculator(),
            'MAX_HALSTEAD_DIFFICULTY':
                difficulty.MaxHalsteadDifficultyCalculator(),
            'MEAN_HALSTEAD_EFFORT':
                effort.MeanHalsteadEffortCalculator(),
            'MAX_HALSTEAD_EFFORT':
                effort.MaxHalsteadEffortCalculator(),
            'MEAN_HALSTEAD_TIME_REQUIRED_TO_PROGRAM':
                time_to_program.MeanHalsteadTimeToProgramCalculator(),
            'MAX_HALSTEAD_TIME_REQUIRED_TO_PROGRAM':
                time_to_program.MaxHalsteadTimeToProgramCalculator(),
            'MEAN_HALSTEAD_NUMBER_OF_DELIVERED_BUGS':
                delivered_bugs.MeanHalsteadDeliveredBugsCalculator(),
            'MAX_HALSTEAD_NUMBER_OF_DELIVERED_BUGS':
                delivered_bugs.MaxHalsteadDeliveredBugsCalculator(),
            'MEAN_MAINTAINABILITY_INDEX':
                MeanMaintainabilityIndexCalculator(),
            'MIN_MAINTAINABILITY_INDEX':
                MinMaintainabilityIndexCalculator(),
            'MEAN_CAMC': MeanCAMCCalculator(),
            'MIN_CAMC': MinCAMCCalculator(),
            'MAX_CAMC': MaxCAMCCalculator(),
            'MEAN_NHD': MeanNHDCalculator(),
            'MIN_NHD': MinNHDCalculator(),
            'MAX_NHD': MaxNHDCalculator(),
            'MEAN_LCOM1': MeanLCOM1Calculator(),
            'MAX_LCOM1': MaxLCOM1Calculator(),
            'MEAN_LCOM2': MeanLCOM2Calculator(),
            'MAX_LCOM2': MaxLCOM2Calculator(),
            'MEAN_LCOM3': MeanLCOM3Calculator(),
            'MAX_LCOM3': MaxLCOM3Calculator(),
            'MEAN_LCOM4': MeanLCOM4Calculator(),
            'MAX_LCOM4': MaxLCOM4Calculator(),
            'MEAN_TCC': MeanTCCCalculator(),
            'MIN_TCC': MinTCCCalculator(),
            'MEAN_LCC': MeanLCCCalculator(),
            'MIN_LCC': MinLCCCalculator(),
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
