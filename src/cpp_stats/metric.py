class Metric:
    '''
    Class that stores metric name and value.
    '''

    def __init__(self, name: str, value: float):
        '''
        Initializes metric.
        
        Parameters:
        name (str): Metric name.
        value (float): Metric value.
        '''
        self.name = name
        self.value = value
