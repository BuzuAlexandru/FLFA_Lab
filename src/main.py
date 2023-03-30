from grammar.Grammar import Grammar
from grammar.Production import Production
from automata.FiniteAutomaton import FiniteAutomaton
from automata.Transition import Transition
from lexer.lexer import grammar_lexer


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
for token in grammar_lexer(text):
    print(token)

text = '''
VN={S, L, D};
'''
for i in grammar_lexer(text):
    print(i)
