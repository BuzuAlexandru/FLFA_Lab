from lexer.lexer import grammar_lexer
from grammar_parser.grammar_parser import parse, print_ast


text = '''
VN={S, L, D},
VT={a, b, c, d, e, f, j},
P={
    S → aS
    S → bS
    S → cD
    S → dL
    S → e
    L → eL
    L → fL
    L → jD
    L → e
    D → eD
    D → d
}
'''

tokens = grammar_lexer(text)
ast = parse(tokens)
print_ast(ast)
