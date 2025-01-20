import clang.cindex
import abc
from metric import Metric

class LanguageContruct(abc.ABC):
    def __init__(self, cursor: clang.cindex.Cursor):
        self.cursor = cursor
    
    @abc.abstractmethod
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass
    
    @abc.abstractmethod
    def add_construct(self, contruct: 'LanguageContruct'):
        pass

class Lambda(LanguageContruct):
    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)
    
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass
    
class Function(LanguageContruct):
    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)
    
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

class Method(LanguageContruct):
    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)
    
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass

class Class(LanguageContruct):
    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)
    
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass
    
class Structure(LanguageContruct):
    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)
    
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass
    
class Namespace(LanguageContruct):
    def __init__(self, cursor: clang.cindex.Cursor):
        super().__init__(cursor)
    
    def get_metrics(self, metrics_names: list[str]) -> list[Metric]:
        pass
    
    def add_construct(self, contruct: LanguageContruct):
        pass
