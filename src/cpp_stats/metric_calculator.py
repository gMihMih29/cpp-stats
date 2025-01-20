import abc
import clang.cindex
from metric import Metric

class MetricCalculator(abc.ABC):
    
    @abc.abstractmethod
    def __call__(self, node: clang.cindex.Cursor) -> list[Metric]:
        pass
        
    @abc.abstractmethod
    def name(self) -> str:
        pass
        
    @abc.abstractmethod
    def observed_cursors(self) -> list[clang.cindex.CursorKind]:
        pass
