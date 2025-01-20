from typing import List

class CppStats(object):

    def __init__(self, path_to_repo: str):
        self._path_to_repo = path_to_repo
        self._available_metrics = [
            'NUMBER_OF_CLASSES',
            'MEAN_NUMBER_OF_METHODS_PER_CLASS',
            'MAX_NUMBER_OF_METHODS_PER_CLASS',
            'MEAN_LENGTH_OF_METHODS',
            'MAX_LENGTH_OF_METHODS',
            'CYCLOMATIC_COMPLEXITY',
            'MEAN_CYCLOMATIC_COMPLEXITY',
            'MAX_CYCLOMATIC_COMPLEXITY', 
            'COGNITIVE_COMPLEXITY', 
            'MEAN_COGNITIVE_COMPLEXITY', 
            'MAX_COGNITIVE_COMPLEXITY', 
            'HALSTEAD_PROGRAM_VOCABULARY',
            'HALSTEAD_PROGRAM_LENGTH',
            'HALSTEAD_CALCULATED_ESTIMATED_PROGRAM_LENGTH',
            'HALSTEAD_VOLUME',
            'HALSTEAD_DIFFICULTY',
            'HALSTEAD_EFFORT',
            'HALSTEAD_TIME_REQUIRED',
            'HALSTEAD_NUMBER_OF_DELIVERED_BUGS',
            'MAINTAINABILITY_INDEX',
            'LCOM',
            'LCOM2',
            'LCOM3',
            'LCOM4',
            'TCC',
            'LCC',
            'CAMC',
            ]
    
    def list(self) -> list[str]:
        return self._available_metrics
    
    def metric(self, metric_name: str):
        pass
    
    def as_xml(self):
        return (
            f'<report>\n'
            f'    <repository name="path">{self.path_to_repo}</repository>\n'
            f'</report>'
        )
