'''
Classes that represent C/C++ language structures.
'''

import abc
from typing import Dict

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric, ClangMetricCalculator

class LanguageContruct(abc.ABC):
    '''
    Class that represents abstract language construct from C/C++.
    '''

    def __init__(self, cursor: clang.cindex.Cursor):
        '''
        Initializes LanguageContruct.
        
        Parameters:
        cursor (clang.cindex.Cursor): Cursor that points to place in 
        Abstract syntax tree of that language construct.
        '''
        self._cursor = cursor
        self._children = Dict[str, LanguageContruct]

    def get_metric(self, calculator: ClangMetricCalculator) -> Metric:
        '''
        Returns list of metrics for this language construct.
        
        Parameters:
        metrics_names (list[str]): List of requested metrics names.
        '''

    def add_construct(self, stack: list[clang.cindex.Cursor]):
        '''
        Adds new language construct as a child of current language 
        construct.
        
        Parameters:
        contruct (LanguageContruct): Language construct to add as a 
        child.
        '''
        if len(stack) == 0:
            return
        cur_cursor = stack.pop()
        cur_construct = self._children.get(cur_cursor.displayname, None)
        if cur_construct is None:
            self._children[cur_cursor.displayname] = cur_construct = _build_lang_contruct(cur_cursor)
        if cur_construct is not None:
            self._children[cur_cursor.displayname].add_construct(stack)

class Lambda(LanguageContruct):
    '''
    Class that represents lambda expression.
    '''

    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)

    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

class Function(LanguageContruct):
    '''
    Class that represents function.
    '''

    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)

    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

class Method(LanguageContruct):
    '''
    Class that represents method of class.
    '''

    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)

    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

class Class(LanguageContruct):
    '''
    Class that represents class from C++.
    '''

    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)

    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

class Structure(LanguageContruct):
    '''
    Class that represents structure.
    '''

    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)

    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

class Namespace(LanguageContruct):
    '''
    Class that represents namespace.
    '''

    def __init__(self, cursor: clang.cindex.Cursor = None):
        super().__init__(cursor)

    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

def _build_lang_contruct(cursor: clang.cindex.Cursor) -> LanguageContruct:
    if cursor.kind == clang.cindex.CursorKind.NAMESPACE:
        return Namespace(cursor)
    if cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
        return Class(cursor)
    if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        return Function(cursor)
    if cursor.kind in [
        clang.cindex.CursorKind.CXX_METHOD,
        clang.cindex.CursorKind.CONSTRUCTOR,
        clang.cindex.CursorKind.DESTRUCTOR
        ]:
        return Method(cursor)
    if cursor.kind == clang.cindex.CursorKind.LAMBDA_EXPR:
        return Lambda(cursor)
    if cursor.kind == clang.cindex.CursorKind.STRUCT_DECL:
        return Structure(cursor)
    return None
