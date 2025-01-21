import abc
import clang.cindex
from metric import Metric

class MetricCalculator(abc.ABC):
    '''
    Class for calculating specific list of metrics.
    '''
    
    @abc.abstractmethod
    def __call__(self, node: clang.cindex.Cursor) -> list[Metric]:
        '''
        Calculates metrics for a given node that represents function, 
        method, class or etc.

        Parameters:
        node (clang.cindex.Cursor): Node for which metrics are 
        calculated.

        Returns:
        list[Metric]: List of metrics calculated for node.
        '''
        
        pass
        
    @abc.abstractmethod
    def observed_cursors(self) -> list[clang.cindex.CursorKind]:
        '''
        Returns list of cursor kinds that can be passed as an argument 
        for __call__.

        Returns:
        list[clang.cindex.CursorKind]: List of observed cursor kinds.
        '''
        
        pass
