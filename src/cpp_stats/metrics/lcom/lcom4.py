'''
Module for MEAN_LCOM4 and MAX_LCOM4 metrics.
'''

from cpp_stats.metrics.lcom.base import LCOMClassData
from cpp_stats.metrics.lcom.base_metric import MaxLCOMMetric, MeanLCOMMetric, LCOMCalculator

MEAN_LCOM4 = 'MEAN_LCOM4'
MAX_LCOM4 = 'MAX_LCOM4'

def _dfs(current: str, graph: dict[str, set[str]], not_used_nodes: set[str]):
    not_used_nodes.remove(current)
    for neighbor in graph[current]:
        if neighbor in not_used_nodes:
            _dfs(neighbor, graph, not_used_nodes)

def _get_lcom4(data: LCOMClassData) -> float:
    graph = {}
    nodes = set([])
    for field in data.fields:
        graph[field] = set([])
        nodes.add(field)
    for key, value in data.method_data.items():
        graph[key] = set([])
        nodes.add(key)
        for field in value.used_fields:
            graph[field] |= set([key])
            graph[key] |= set([field])
        for method in value.used_methods:
            graph[key] |= set([method])
            if method in graph:
                graph[method] |= set([key])
            else:
                graph[method] = set([key])

    not_used_nodes = nodes.copy()
    res = 0
    for node in nodes:
        if node in not_used_nodes:
            _dfs(node, graph, not_used_nodes)
            res += 1

    return res

class MeanLCOM4Metric(MeanLCOMMetric):
    '''
    Represents MEAN_LCOM4 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom4(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MEAN_LCOM4,
            MeanLCOM4Metric,
            data
        )

# pylint: disable=R0903
class MeanLCOM4Calculator(LCOMCalculator):
    '''
    Calculates MEAN_LCOM4.
    '''

    def __init__(self):
        super().__init__(
            MeanLCOM4Metric
        )

class MaxLCOM4Metric(MaxLCOMMetric):
    '''
    Represents MAX_LCOM4 metric.
    '''

    @classmethod
    def value_source(cls, lcom_data: LCOMClassData):
        return _get_lcom4(lcom_data)

    def __init__(self, data: dict[str, LCOMClassData]):
        super().__init__(
            MAX_LCOM4,
            MaxLCOM4Metric,
            data
        )

# pylint: disable=R0903
class MaxLCOM4Calculator(LCOMCalculator):
    '''
    Calculates MAX_LCOM4.
    '''

    def __init__(self):
        super().__init__(
            MaxLCOM4Metric
        )
