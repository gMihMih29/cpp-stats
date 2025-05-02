'''
Contains main logic for calculating LCOM metrics.
'''

import cmath

from clang.cindex import CursorKind, Cursor

from cpp_stats.metrics.utils import mangle_cursor_name

class LCOMMethodData:
    '''
    Contains methods and fields which are used by method 'method_name'.
    '''

    def __init__(self,
                 method_name: str,
                 used_methods: set[str] = None,
                 used_fields: set[str] = None):
        self.method_name = method_name
        if used_methods is None:
            used_methods = set([])
        if used_fields is None:
            used_fields = set([])
        self.used_methods = used_methods
        self.used_fields = used_fields

class LCOMClassData:
    '''
    Contains information about used methods and fields
    for each viewed method for class 'class_name'.
    '''

    def __init__(self,
                 class_name: str,
                 method_data: dict[str, LCOMMethodData],
                 fields: set[str]):
        self.class_name = class_name
        self.method_data = method_data
        self.fields = fields

    def __add__(self, other):
        if not isinstance(other, LCOMClassData):
            raise NotImplementedError
        if self.class_name != other.class_name:
            raise RuntimeError
        new_dict = {}
        for key, value in self.method_data.items():
            new_dict[key] = value
        for key, value in other.method_data.items():
            new_dict[key] = value
        return LCOMClassData(self.class_name, new_dict, self.fields | other.fields)

def get_lcom_data(cursor: Cursor) -> LCOMClassData:
    '''
    Returns prepared data for LCOM calculations for given cursor.
    '''
    class_name = mangle_cursor_name(cursor.semantic_parent)
    if cursor.kind == CursorKind.FIELD_DECL:
        return LCOMClassData(class_name, {}, set([cursor.spelling]))
    method_data = LCOMMethodData(cursor.mangled_name)
    for node in cursor.walk_preorder():
        if node.kind != CursorKind.MEMBER_REF_EXPR or node.referenced is None:
            continue
        if node.referenced.kind == CursorKind.CXX_METHOD:
            method_data.used_methods |= set([node.referenced.mangled_name])
        if node.referenced.kind == CursorKind.FIELD_DECL:
            method_data.used_fields |= set([node.referenced.spelling])
    return LCOMClassData(
        class_name,
        {
            cursor.mangled_name: method_data
        },
        set([])
    )

def merge_class_lcom_data(lhv: dict[str, LCOMClassData], rhv: dict[str, LCOMClassData]):
    '''
    Merges two dictionary by class names as keys.
    '''
    new_dict = {}
    for key, value in lhv.items():
        new_dict[key] = value
    for key, value in rhv.items():
        if new_dict.get(key, None) is None:
            new_dict[key] = value
        else:
            new_dict[key] += value
    return new_dict

