import clang.cindex

import cmath

class HalsteadData:
    def __init__(self, n1: set[str], n2: set[str], N1: int, N2: int):
        self.n1 = n1
        self.n2 = n2
        self.N1 = N1
        self.N2 = N2

    def __add__(self, other):
        if not isinstance(other, HalsteadData):
            raise NotImplementedError
        return HalsteadData(self.n1 | other.n1, self.n2 | other.n2, self.N1 + other.N1, self.N2 + other.N2)

    def program_vocabulary(self):
        return len(self.n1) + len(self.n2)

    def program_length(self):
        return self.N1 + self.N2
    
    def estimated_length(self):
        return len(self.n1) * cmath.log(len(self.n1), 2) + len(self.n2) * cmath.log(len(self.n2), 2)

    def volume(self):
        return self.program_length() * cmath.log(self.program_vocabulary(), 2)
    
    def difficulty(self):
        return len(self.n1) / 2 * self.N2 / len(self.n2)
    
    def effort(self):
        return self.difficulty() * self.volume()
    
    def time_required_to_program(self):
        return self.effort() / 18
    
    def delivered_bugs(self):
        return self.volume() / 3000

def __is_operator(cursor):
    return cursor.kind in [
        clang.cindex.CursorKind.BINARY_OPERATOR,
        clang.cindex.CursorKind.UNARY_OPERATOR,
        clang.cindex.CursorKind.CALL_EXPR,
        clang.cindex.CursorKind.COMPOUND_STMT,
        clang.cindex.CursorKind.DECL_REF_EXPR,
    ]

def __is_operand(cursor):
    return cursor.kind in [
        clang.cindex.CursorKind.INTEGER_LITERAL,
        clang.cindex.CursorKind.FLOATING_LITERAL,
        clang.cindex.CursorKind.IMAGINARY_LITERAL,
        clang.cindex.CursorKind.CHARACTER_LITERAL,
        clang.cindex.CursorKind.STRING_LITERAL,
        clang.cindex.CursorKind.COMPOUND_LITERAL_EXPR,
        clang.cindex.CursorKind.CXX_BOOL_LITERAL_EXPR,
        clang.cindex.CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
        clang.cindex.CursorKind.CXX_THIS_EXPR,
        clang.cindex.CursorKind.VAR_DECL
    ]

def create_data(node: clang.cindex.Cursor) -> HalsteadData:
    result = HalsteadData(set(), set(), 0, 0)
    if __is_operator(node):
        result.n1 |= set(node.displayname)
        result.N1 += 1
    if __is_operand(node):
        result.n2 |= set(node.displayname)
        result.N2 += 1
    return result

def merge_data(lhv: dict[str, HalsteadData], rhv: dict[str, HalsteadData]):
    new_data = {}
    for file_name, halstead_data in lhv.items():
        new_data[file_name] = halstead_data
    for file_name, halstead_data in rhv.items():
        if new_data.get(file_name, None) is None:
            new_data[file_name] = halstead_data
        else:
            new_data[file_name] += halstead_data
    return new_data

def HalsteadMetric(Metric):
    def __init__():
        pass
