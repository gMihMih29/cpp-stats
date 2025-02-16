from pathlib import Path

from cpp_stats.metrics.metric_calculator import BasicMetricCalculator
from cpp_stats.metrics.metric import Metric

class LinesOfCodeCalculator(BasicMetricCalculator):
    '''
    Calculates LINES_OF_CODE.
    '''
    CALCULATED_METRIC_NAME = 'LINES_OF_CODE'

    def __call__(self, file_paths: list[Path]) -> list[Metric]:
        cnt = 0
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                while f.readline():
                    cnt += 1
        return Metric(LinesOfCodeCalculator.CALCULATED_METRIC_NAME, cnt)
                