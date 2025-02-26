'''
Classes that represent C/C++ language structures.
'''

import abc

import clang.cindex

from cpp_stats.metrics.metric_calculator import Metric

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
        self.cursor = cursor

    @abc.abstractmethod
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        '''
        Returns list of metrics for this language construct.
        
        Parameters:
        metrics_names (list[str]): List of requested metrics names.
        '''
    @abc.abstractmethod
    def add_construct(self, contruct: 'LanguageContruct'):
        '''
        Adds new language construct as a child of current language 
        construct.
        
        Parameters:
        contruct (LanguageContruct): Language construct to add as a 
        child.
        '''

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

    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)

    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass
