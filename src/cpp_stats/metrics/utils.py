'''
Module for helper functions
'''

import clang.cindex

def mangle_cursor_name(node: clang.cindex.Cursor) -> str:
    '''
    Returns string that contains full name of node with parent classes, namespaces and etc.
    
    Example:
    `::ThreeDRenderer::Camera`
    
    Parameters:
    node (clang.cindex.Cursor): cursor for which mangled name is being calculated.
    '''
    if node.kind == clang.cindex.CursorKind.TRANSLATION_UNIT:
        return ""
    return mangle_cursor_name(node.semantic_parent) + '::' + node.displayname
