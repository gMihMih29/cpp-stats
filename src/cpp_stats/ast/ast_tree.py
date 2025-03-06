'''
Module for creating ast tree based on clang tree for calculating metric.
'''

from pathlib import Path

import clang.cindex

from cpp_stats.metrics.metric_calculator import ClangMetricCalculator, Metric
from cpp_stats.ast.language import Namespace

def get_ast_tree(c_cxx_files: list[Path]) -> Namespace:
    '''
    Constructs ast based on files given in arguments.
    
    Parameters:
    c_cxx_files (list[Path]): C/C++ files to parse.
    '''
    # Path will be configurable in config.yaml
    clang.cindex.Config.set_library_file('D:\\Program_Files\\mingw64\\bin\\libclang.dll')
    index = clang.cindex.Index.create()
    global_namespace = Namespace()
    for i, file_path in enumerate(c_cxx_files):
        translation_unit = index.parse(file_path, args=['-x', 'c++'])
        _parse_children(
            global_namespace,
            translation_unit.cursor,
            str(file_path.resolve())
        )
    return global_namespace

def _parse_children(
    global_namespace: Namespace,
    current: clang.cindex.Cursor,
    analyzed_file: str
    ):
    for child in current.get_children():
        if child.location.file is None or child.location.file.name != analyzed_file:
            continue
        semantic_parents_stack = []
        cur = child
        while cur is not None and cur.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            semantic_parents_stack.append(cur)
            cur = cur.semantic_parent
        global_namespace.add_construct(semantic_parents_stack)
        _parse_children(global_namespace, child, analyzed_file)

def analyze_ast(c_cxx_files: list[Path], calculators: dict[str, ClangMetricCalculator]) -> dict[str, Metric]:
    '''
    Analyzes ast based on `c_cxx_files` and calculates metrics using `calculators`
    
    Parameters:
    `c_cxx_files` (`list[Path]`): C/C++ files to parse.
    `calculators` (`list[ClangMetricCalculator]`): calculators to calculate metris.
    
    Returns:
    `dict[str, Metric]`: dictionary with all metrics calculated by `calculators`.
    '''
    clang.cindex.Config.set_library_file('D:\\Program_Files\\mingw64\\bin\\libclang.dll')
    index = clang.cindex.Index.create()
    result = dict()
    for i, file_path in enumerate(c_cxx_files):
        translation_unit = index.parse(file_path, args=['-x', 'c++'])
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
    for child in cursor.get_children():
        if child.location.file is None or child.location.file.name != analyzed_file:
            continue
        for clc in calculators.items():
            metric = clc[1](child)
            if result.get(metric.name(), None) is None:
                result[metric.name()] = metric
            else:
                result[metric.name()] += metric
        _analyze_children(result, calculators, child, analyzed_file)
