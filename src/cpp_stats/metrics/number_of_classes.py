'''
Module for NUMBER_OF_CLASSES metric.
'''

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

METRIC_NAME = 'NUMBER_OF_CLASSES'

class NumberOfClassesMetric(Metric):
    '''
    Represents NUMBER_OF_CLASSES metric.
    '''
    def __init__(self, names: set):
        '''
        Initializes metric.
        
        Parameters:
        value (float): Metric value.
        '''
        super().__init__(METRIC_NAME)
        self.names = names

    def __add__(self, other):
        if not isinstance(other, NumberOfClassesMetric):
            raise NotImplementedError
        return NumberOfClassesMetric(self.names | other.names)

    def get(self) -> tuple[str, float]:
        '''
        Returns metric value.
        '''
        return METRIC_NAME, len(self.names)

class NumberOfClassesCalculator(ClangMetricCalculator):
    '''
    Calculates NUMBER_OF_CLASSES.
    '''

    def __call__(self, node: clang.cindex.Cursor) -> Metric:
        if node.kind != clang.cindex.CursorKind.CLASS_DECL and node.get_definition() is not None:
            return NumberOfClassesMetric(set([]))
        name = node.displayname
        cur = node.semantic_parent
        while cur.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            name += f"::{cur.displayname}"
            cur = cur.semantic_parent
        return NumberOfClassesMetric(set([name]))

    def observed_cursors(self) -> list[clang.cindex.CursorKind]:
        '''
        Returns list of cursor kinds that can be passed as an argument 
        for __call__.

        Returns:
        list[clang.cindex.CursorKind]: List of observed cursor kinds.
        '''
        return [clang.cindex.CursorKind.CLASS_DECL]
                