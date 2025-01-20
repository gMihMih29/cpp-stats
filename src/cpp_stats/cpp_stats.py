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
            'HALSTEAD_COMPLEXITY',
            'MAINTAINABILITY_INDEX',
            'LCOM',
            'LACK_OF_COHESION_OF_METHODS',
            'LCOM2',
            'LACK_OF_COHESION_OF_METHODS2',
            'LCOM3',
            'LACK_OF_COHESION_OF_METHODS3',
            'LCOM4',
            'LACK_OF_COHESION_OF_METHODS4',
            'TCC',
            'TIGHT_CLASS_COHESION',
            'LCC',
            'LOOSE_CLASS_COHESION',
            'CAMC',
            'COHESION_AMONG_METHODS_OF_A_CLASS',
            'NHD',
            'NORMALIZED_HAMMING_DISTANCE'
        ]
    
    def list(self) -> List[str]:
        return self._available_metrics
    
    def metric(self, metric_name: str):
        pass
    
    def as_xml(self):
        return (
            f'<report>\n'
            f'    <repository name="path">{self.path_to_repo}</repository>\n'
            f'</report>'
        )
