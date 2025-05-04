'''
Contains base logic for work with argument types of methods.
'''

import clang.cindex

from cpp_stats.metrics.utils import mangle_cursor_name


def _merge_class_data(lhv: dict[str, set[str]], rhv: dict[str, set[str]]):
    '''
    Merges two dictionaries that contain set of argument types for each method of class.
    '''
    result = {}
    for key, item in lhv.items():
        result[key] = item
    for key, item in rhv.items():
        result[key] = item
    return result

def merge_argument_data(lhv: dict[str, dict[str, set[str]]], rhv: dict[str, dict[str, set[str]]]):
    '''
    Merges two dictionaries that contain set of argument types for each viewed method
    for each viewed class.
    '''
    result = {}
    for key, item in lhv.items():
        result[key] = item
    for key, item in rhv.items():
        if result.get(key, None) is None:
            result[key] = item
        else:
            result[key] = _merge_class_data(result[key], item)
    return result

def _get_set_of_argument_types(method: clang.cindex.Cursor) -> set[str]:
    '''
    Returns set of argument types for given method.
    
    First key of result dictionary is mangled name of method.
    '''
    result = set([])
    for child in method.get_children():
        if child.kind == clang.cindex.CursorKind.COMPOUND_STMT:
            break
        if child.kind == clang.cindex.CursorKind.PARM_DECL:
            result |= set([child.type.spelling])
    return result

def get_argument_data(method: clang.cindex.Cursor):
    '''
    Returns set of argument types for given method.
    
    First key of result dictionary is name of class with all namespaces.
    Second key of result dictionary is mangled name of method.
    '''
    return {
        mangle_cursor_name(method.semantic_parent): {
            method.mangled_name: _get_set_of_argument_types(method)
        }
    }
