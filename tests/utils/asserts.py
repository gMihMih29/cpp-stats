'''
Contains useful asserts.
'''

def assert_lists_equal_unordered(expected, actual):
    '''
    Asserts that two lists contain same elements.
    
    Parameters:
    `expected` (list): Expected list.
    `actual` (list): List to check.
    '''
    assert sorted(expected) == sorted(actual), f"Expected: {expected}, Actual: {actual}"
