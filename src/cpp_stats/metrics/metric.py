class Metric:
    '''
    Class that stores metric name and value.
    '''

    def __init__(self, name: str, value: float, count: int = 1):
        '''
        Initializes metric.
        
        Parameters:
        name (str): Metric name.
        value (float): Metric value.
        '''
        self.name = name
        self.value = value
        self.count = count

    def __add__(self, other):
        if not isinstance(other, Metric):
            return NotImplemented
        if self.name != other.name:
            return NotImplemented
        return Metric(self.name, self.value + other.value, self.count + other.count)

    def get(self):
        '''
        Returns metric value. Should be called since metric can be summarization of many files,
        namespaces, classes and etc.
        '''
        return self.value / self.count
