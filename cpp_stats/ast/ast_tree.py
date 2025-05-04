'''
Module for creating ast tree based on clang tree for calculating metric.
'''

from pathlib import Path
import os

import clang.cindex

from cpp_stats.metrics.metric_calculator import ClangMetricCalculator, Metric

def analyze_ast(index: clang.cindex.Index, repo_path: str, c_cxx_files: list[Path],
                calculators: dict[str, ClangMetricCalculator]) -> dict[str, Metric]:
    '''
    Analyzes ast based on `c_cxx_files` and calculates metrics using `calculators`
    
    Parameters:
    `c_cxx_files` (`list[Path]`): C/C++ files to parse.
    `calculators` (`list[ClangMetricCalculator]`): calculators to calculate metris.
    
    Returns:
    `dict[str, Metric]`: dictionary with all metrics calculated by `calculators`.
    '''
    result = {}
    args = ["-x", "c++"]
    for root, _, _ in os.walk(repo_path):
        args.extend(["-I", root])
    for _, file_path in enumerate(c_cxx_files):
        translation_unit = index.parse(file_path, args=args)
        _analyze_children(
            result,
            calculators,
            translation_unit.cursor,
            str(file_path.resolve())
        )
    return result

def _analyze_children(
    result: dict[str, Metric],
    calculators: dict[str, ClangMetricCalculator],
    cursor: clang.cindex.Cursor,
    analyzed_file: str
    ):
    for clc in calculators.items():
        metric = clc[1](cursor)
        if result.get(metric.name(), None) is None:
            result[metric.name()] = metric
        else:
            result[metric.name()] += metric
    for child in cursor.get_children():
        if (not child.kind.is_translation_unit() and
            (child.location.file is None or
            child.translation_unit.spelling != child.location.file.name)):
            continue
        _analyze_children(result, calculators, child, analyzed_file)
