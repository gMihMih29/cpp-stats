import cmath
import re

from clang.cindex import CursorKind, Cursor

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

def __is_literal(cursor):
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

def __get_literal_spelling(literal: Cursor) -> str:
    start = literal.extent.start
    end = literal.extent.end
    with open(start.file.name, "r", encoding="utf-8") as source_code:
        for i in range(start.line):
            literal_str = source_code.readline()
    literal_str = literal_str[start.column - 1: end.column - 1]
    return literal_str

def create_data(node: Cursor) -> HalsteadData:
    result = HalsteadData(set(), set(), 0, 0)
    
    # method or func call
    if node.kind == CursorKind.CALL_EXPR:
        result.n1 |= set([node.displayname])
        result.N1 += 1
    
    # methods
    if node.kind == CursorKind.CXX_METHOD:
        result.n1 |= set([node.mangled_name])
        result.N1 += 1
    # type names
    if node.kind == CursorKind.TYPE_REF:
        result.n1 |= set([node.displayname])
        result.N1 += 1

    # funcs
    if node.kind == CursorKind.FUNCTION_DECL:
        result.n1 |= set([node.mangled_name])
        result.N1 += 1
    
    # Parameters
    if node.kind == CursorKind.PARM_DECL:
        result.n2 |= set([node.mangled_name])
        result.N2 += 1
        
    # variables
    if node.kind == CursorKind.VAR_DECL:
        result.n2 |= set([node.mangled_name])
        result.N2 += 1
        
    # fields
    if node.kind == CursorKind.FIELD_DECL:
        result.n2 |= set([node.mangled_name])
        result.N2 += 1
    
    # if __is_operator(node):
    #     result.n1 |= set([node.displayname])
    #     result.N1 += 1
    if __is_literal(node):
        if node.spelling != "":
            result.n2 |= set([node.spelling])
        else:
            result.n2 |= set([__get_literal_spelling(node)])
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

def find_remaining_operators(file_path: str) -> HalsteadData:
    operators_re = r'(\+=)|(/=)|(-=)|(\*=)|(->)|(\+=)|(\+=)|(,)|(;)|(\+)|(-)|(\*)|(/)|(=)|({)|(^)|(%)|(\[)|(\.)|(>=)|(>)|(<=)|(<)|(\()|(&)'
    # match = re.search(r'//', input_string)
    distinct_operators = set([])
    operators_cnt = 0
    with open(file_path, "r", encoding="utf-8") as source_code:
        line = source_code.readline()
        while line != "":
            # For comments
            match = re.search(r'//', line)
            if match:
                line = line[: match.start()]
            # For preprocessor commads
            match = re.search(r'#', line)
            if match:
                line = line[: match.start()]
            matches = re.findall(operators_re, line)
            if matches:
                for group in matches:
                    for gr in group:
                        if gr is None or gr == "":
                            continue
                        distinct_operators |= set([gr])
                operators_cnt += len(matches)
            line = source_code.readline()
    return HalsteadData(distinct_operators, set([]), operators_cnt, 0)
