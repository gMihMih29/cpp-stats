'''
Contains main logic for calculating Halstead complexity including number of operators and operands.
'''

import cmath

from clang.cindex import CursorKind, Cursor

from cpp_stats.metrics.utils import mangle_cursor_name

class HalsteadData:
    '''
    Stores information about viewed operators and operands
    '''

    # pylint: disable=C0103
    def __init__(self, n1: set[str], n2: set[str], N1: int, N2: int):
        self.n1 = n1
        self.n2 = n2
        self.N1 = N1
        self.N2 = N2

    def __add__(self, other):
        if not isinstance(other, HalsteadData):
            raise NotImplementedError
        return HalsteadData(
            self.n1 | other.n1,
            self.n2 | other.n2,
            self.N1 + other.N1,
            self.N2 + other.N2
        )

    def program_vocabulary(self):
        '''
        Calculates Halstead program vocabulary.
        '''
        return len(self.n1) + len(self.n2)

    def program_length(self):
        '''
        Calculates Halstead program length.
        '''
        return self.N1 + self.N2

    def estimated_length(self):
        '''
        Calculates Halstead estimated length of program.
        '''
        return len(self.n1) * cmath.log(len(self.n1), 2) + len(self.n2) * cmath.log(len(self.n2), 2)

    def volume(self):
        '''
        Calculates Halstead volume.
        '''
        return self.program_length() * cmath.log(self.program_vocabulary(), 2)

    def difficulty(self):
        '''
        Calculates Halstead difficulty.
        '''
        return len(self.n1) / 2 * self.N2 / len(self.n2)

    def effort(self):
        '''
        Calculates Halstead effort.
        '''
        return self.difficulty() * self.volume()

    def time_required_to_program(self):
        '''
        Calculates Halstead time required to program.
        '''
        return self.effort() / 18

    def delivered_bugs(self):
        '''
        Calculates Halstead delivered bugs.
        '''
        return self.volume() / 3000

def __is_literal(cursor):
    '''
    Checks that given cursor is literal.
    '''
    return cursor.kind in [
        CursorKind.INTEGER_LITERAL,
        CursorKind.FLOATING_LITERAL,
        CursorKind.IMAGINARY_LITERAL,
        CursorKind.CHARACTER_LITERAL,
        CursorKind.STRING_LITERAL,
        CursorKind.COMPOUND_LITERAL_EXPR,
        CursorKind.CXX_BOOL_LITERAL_EXPR,
        CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
        CursorKind.CXX_THIS_EXPR
    ]

def __get_spelling(cursor: Cursor) -> str:
    '''
    Gets spelling of cursor directly from source file.
    '''
    start = cursor.extent.start
    end = cursor.extent.end
    with open(start.file.name, "r", encoding="utf-8") as source_code:
        for _ in range(start.line):
            cursor_str = source_code.readline()
    cursor_str = cursor_str[start.column - 1: end.column - 1]
    return cursor_str

def __get_literal_spelling(cursor: Cursor):
    tokens = list(cursor.get_tokens())
    op_token = tokens[0]
    return op_token.spelling

def __get_binary_operator_spelling(cursor):
    children = list(cursor.get_children())
    left_child = children[0]
    tokens = list(cursor.get_tokens())
    left_tokens = list(left_child.get_tokens())
    op_token_index = len(left_tokens)
    op_token = tokens[op_token_index]
    return op_token.spelling

def __get_unary_operator_spelling(cursor):
    tokens = list(cursor.get_tokens())
    op_token = tokens[0]
    return op_token.spelling

def __find_remaining_operators(cursor: Cursor):
    observed_tokens = [',', '::', ';']
    result = HalsteadData(set(), set(), 0, 0)
    for token in cursor.get_tokens():
        if token.spelling in observed_tokens:
            result.n1 |= set([token.spelling])
            result.N1 += 1
            print(token.spelling)
    return result

def create_data(node: Cursor) -> HalsteadData:
    '''
    Analyzes given cursor and checks whether it is operator or operand.
    '''

    result = HalsteadData(set(), set(), 0, 0)

    if node.lexical_parent is not None and node.lexical_parent.kind == CursorKind.TRANSLATION_UNIT:
        result += __find_remaining_operators(node)

    if node.kind in [
        CursorKind.NAMESPACE,
        CursorKind.NAMESPACE_ALIAS,
        CursorKind.USING_DECLARATION,
        CursorKind.CXX_BASE_SPECIFIER,
        CursorKind.NAMESPACE_REF
        ]:
        result.n1 |= set([node.spelling])
        result.N1 += 1

    if node.kind == CursorKind.USING_DIRECTIVE:
        result.n1 |= set(["using namespace"])
        result.N1 += 1

    if node.kind == CursorKind.COMPOUND_STMT:
        result.n1 |= set(["{}"])
        result.N1 += 1

    if node.kind == CursorKind.ARRAY_SUBSCRIPT_EXPR:
        result.n1 |= set(["[]"])
        result.N1 += 1

    if node.kind == CursorKind.INIT_LIST_EXPR:
        result.n1 |= set(["{}"])
        result.N1 += 1

    if node.kind == CursorKind.PAREN_EXPR:
        result.n1 |= set(["operator()"])
        result.N1 += 1

    if node.kind == CursorKind.CONDITIONAL_OPERATOR:
        result.n1 |= set(["?;"])
        result.N1 += 1

    if node.kind == CursorKind.ADDR_LABEL_EXPR:
        result.n1 |= set(["&&"])
        result.N1 += 1 # void* ptr = &&target_label;

    if node.kind == CursorKind.CALL_EXPR:
        # result.n1 |= set([node.referenced.mangled_name])
        result.n1 |= set(["operator()"])
        result.N1 += 1

    if node.kind in [
        CursorKind.CSTYLE_CAST_EXPR,
        CursorKind.CXX_FUNCTIONAL_CAST_EXPR
        ]:
        result.n1 |= set(["operator()"])
        result.n1 |= set([node.type.spelling])
        result.N1 += 2

    # if node.kind == CursorKind.CXX_FUNCTIONAL_CAST_EXPR:
    #     result.n1 |= set(["operator()"])
    #     result.n1 |= set([node.type.spelling])
    #     result.N1 += 2

    if node.kind == CursorKind.CXX_METHOD:
        result.n1 |= set([node.mangled_name])
        result.N1 += 1

    if node.kind == CursorKind.CASE_STMT:
        result.n1 |= set(["case"])
        result.N1 += 1
    if node.kind == CursorKind.DEFAULT_STMT:
        result.n1 |= set(["default"])
        result.N1 += 1
    if node.kind == CursorKind.IF_STMT:
        result.n1 |= set(["if"])
        result.N1 += 1
    if node.kind == CursorKind.SWITCH_STMT:
        result.n1 |= set(["switch"])
        result.N1 += 1
    if node.kind == CursorKind.WHILE_STMT:
        result.n1 |= set(["while"])
        result.N1 += 1
    if node.kind == CursorKind.DO_STMT:
        result.n1 |= set(["do"])
        result.n1 |= set(["while"])
        result.N1 += 2
    if node.kind == CursorKind.FOR_STMT:
        result.n1 |= set(["for"])
        result.N1 += 1
    if node.kind in [
        CursorKind.GOTO_STMT,
        CursorKind.INDIRECT_GOTO_STMT
        ]:
        result.n1 |= set(["goto"])
        result.N1 += 1
    if node.kind == CursorKind.CONTINUE_STMT:
        result.n1 |= set(["continue"])
        result.N1 += 1
    if node.kind == CursorKind.BREAK_STMT:
        result.n1 |= set(["break"])
        result.N1 += 1
    if node.kind == CursorKind.RETURN_STMT:
        result.n1 |= set(["return"])
        result.N1 += 1
    if node.kind == CursorKind.ASM_STMT:
        result.n1 |= set(["asm"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_CATCH_STMT:
        result.n1 |= set(["catch"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_TRY_STMT:
        result.n1 |= set(["try"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_FOR_RANGE_STMT:
        result.n1 |= set(["for"])
        result.n1 |= set([":"])
        result.N1 += 2
    if node.kind == CursorKind.NULL_STMT:
        result.n1 |= set(["try"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_FINAL_ATTR:
        result.n1 |= set(["final"])
        result.N1 += 1
    if node.kind == CursorKind.ALIGNED_ATTR:
        result.n1 |= set(["alignas"])
        result.N1 += 1
    if node.kind == CursorKind.WARN_UNUSED_RESULT_ATTR:
        result.n1 |= set(["[[nodiscard]]"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_OVERRIDE_ATTR:
        result.n1 |= set(["override"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_STATIC_CAST_EXPR:
        result.n1 |= set(["static_cast"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_DYNAMIC_CAST_EXPR:
        result.n1 |= set(["dynamic_cast"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_DYNAMIC_CAST_EXPR:
        result.n1 |= set(["reinterpret_cast"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_CONST_CAST_EXPR:
        result.n1 |= set(["const_cast"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_TYPEID_EXPR:
        result.n1 |= set(["typeid"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_THROW_EXPR:
        result.n1 |= set(["throw"])
        result.N1 += 1
    if node.kind == CursorKind.CXX_NEW_EXPR:
        result.n1 |= set(["new"])
        result.N1 += 1
    if node.kind == CursorKind.PACK_EXPANSION_EXPR:
        result.n1 |= set(["..."])
        result.n1 |= set(["{}"])
        result.N1 += 2
    if node.kind == CursorKind.SIZE_OF_PACK_EXPR:
        result.n1 |= set(["sizeof..."])
        result.n1 |= set(["operator()"])
        result.N1 += 2
    if node.kind == CursorKind.LAMBDA_EXPR:
        result.n1 |= set(["[]"])
        result.n1 |= set(["operator()"])
        result.n1 |= set(["{}"])
        result.N1 += 3
    if node.kind == CursorKind.CXX_ACCESS_SPEC_DECL:
        result.n1 |= set([__get_unary_operator_spelling(node)])
        result.N1 += 1

    if node.kind in [
        CursorKind.CONSTRUCTOR,
        CursorKind.DESTRUCTOR
        ]:
        result.n1 |= set([node.spelling])
        result.N1 += 1

    if node.kind in [
        CursorKind.CLASS_DECL,
        CursorKind.STRUCT_DECL,
        CursorKind.UNION_DECL,
        CursorKind.ENUM_DECL,
        CursorKind.CLASS_TEMPLATE,
        CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION
        ]:
        result.n1 |= set([node.spelling])
        result.N1 += 1

    if node.kind in [
        CursorKind.TYPE_REF,
        CursorKind.TYPE_ALIAS_DECL,
        CursorKind.TYPEDEF_DECL,
        CursorKind.TEMPLATE_REF
        ]:
        result.n1 |= set([node.displayname])
        result.N1 += 1

    if node.kind in [
        CursorKind.FUNCTION_DECL,
        CursorKind.CONVERSION_FUNCTION,
        CursorKind.FUNCTION_TEMPLATE
        ]:
        result.n1 |= set([node.mangled_name])
        result.n1 |= set(["operator()"])
        result.N1 += 2

    if node.kind == CursorKind.PARM_DECL:
        if len(list(node.get_tokens())) == 2:
            result.n1 |= set([node.type.spelling])
            result.N1 += 1
        result.n2 |= set([node.mangled_name])
        result.N2 += 1

    if node.kind in [CursorKind.LABEL_REF, CursorKind.LABEL_STMT]:
        result.n2 |= set([node.spelling])
        result.N2 += 1
        result.n1 |= set([":"])
        result.N1 += 1

    if node.kind == CursorKind.VAR_DECL:
        if len(list(node.get_tokens())) == 2:
            result.n1 |= set([node.type.spelling])
            result.N1 += 1
        result.n2 |= set([node.mangled_name])
        result.N2 += 1

    if node.kind == CursorKind.FIELD_DECL:
        result.n2 |= set([mangle_cursor_name(node)])
        result.N2 += 1

    if node.kind == CursorKind.TEMPLATE_NON_TYPE_PARAMETER:
        result.n2 |= set([mangle_cursor_name(node)])
        result.N2 += 1

    if node.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
        spelling = mangle_cursor_name(node)
        if node.spelling == '':
            spelling += "::" + __get_spelling(node)
        result.n1 |= set([spelling])
        result.N1 += 1

    if node.kind == CursorKind.MEMBER_REF_EXPR:
        result.n2 |= set([mangle_cursor_name(node.referenced)])
        result.N2 += 1
        result.n1 |= set([__get_binary_operator_spelling(node)])
        result.N1 += 1

    if node.kind in [
        CursorKind.BINARY_OPERATOR,
        CursorKind.COMPOUND_ASSIGNMENT_OPERATOR
        ]:
        if node.displayname != "":
            result.n1 |= set([node.spelling])
        else:
            spelling = __get_binary_operator_spelling(node)
            if "operator" not in spelling:
                spelling = "operator" + spelling
            result.n1 |= set([spelling])
        result.N1 += 1

    if node.kind == CursorKind.UNARY_OPERATOR:
        if node.displayname != "":
            result.n1 |= set([node.spelling])
        else:
            spelling = __get_unary_operator_spelling(node)
            if "operator" not in spelling:
                spelling = "operator" + spelling
            result.n1 |= set([spelling])
        result.N1 += 1

    if __is_literal(node) or node.kind == CursorKind.ENUM_CONSTANT_DECL:
        if node.spelling != "":
            result.n2 |= set([node.spelling])
        else:
            result.n2 |= set([__get_literal_spelling(node)])
        result.N2 += 1

    if node.kind == CursorKind.DECL_REF_EXPR and node.referenced is not None:
        if node.referenced.kind in [
            CursorKind.VAR_DECL,
            CursorKind.FIELD_DECL,
            CursorKind.PARM_DECL,
            CursorKind.TEMPLATE_NON_TYPE_PARAMETER
            ]:
            result.n2 |= set([node.referenced.mangled_name])
            result.N2 += 1
        else:
            result.n1 |= set([node.referenced.mangled_name])
            result.N1 += 1

    if result.N1 != 0:
        text = f"{node.kind} "
        for token in node.get_tokens():
            text += f" {token.spelling}"
        print(text)

    return result

def merge_data(lhv: dict[str, HalsteadData], rhv: dict[str, HalsteadData]):
    '''
    Merges halstead data according to file names.
    '''
    new_data = {}
    for file_name, halstead_data in lhv.items():
        new_data[file_name] = halstead_data
    for file_name, halstead_data in rhv.items():
        if new_data.get(file_name, None) is None:
            new_data[file_name] = halstead_data
        else:
            new_data[file_name] += halstead_data
    return new_data
