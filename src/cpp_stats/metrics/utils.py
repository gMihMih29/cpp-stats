'''
Module for helper functions
'''

import clang.cindex

def mangle_cursor_name(node: clang.cindex.Cursor) -> str:
    if node.kind == clang.cindex.CursorKind.TRANSLATION_UNIT:
        return ""
    return mangle_cursor_name(node.semantic_parent) + '::' + node.displayname
