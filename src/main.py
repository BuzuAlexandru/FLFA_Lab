from grammar.Grammar import Grammar
from grammar.Production import Production
from automata.FiniteAutomaton import FiniteAutomaton
from automata.Transition import Transition
from lexer.lexer import grammar_lexer

vn = ['S', 'A', 'B', 'C', 'D']
vt = ['a', 'b']
p = [
    Production('S', 'aB'),
    Production('S', 'bA'),
    Production('S', 'A'),
    Production('A', 'B'),
    Production('A', 'AS'),
    Production('A', 'bBAB'),
    Production('A', 'b'),
    Production('B', 'b'),
    Production('B', 'bS'),
    Production('B', 'aD'),
    Production('B', 'ε'),
    Production('D', 'AA'),
    Production('C', 'Ba'),
]

vn1 = ['S', 'A', 'B', 'D', 'Z ']
vt1 = ['a', 'b', 'd']
p1 = [
    Production('S', 'dB'),
    Production('S', 'AB'),
    Production('A', 'd'),
    Production('A', 'dS'),
    Production('A', 'aAaAb'),
    Production('A', 'ε'),
    Production('B', 'a'),
    Production('B', 'aS'),
    Production('B', 'A'),
    Production('D', 'Aba'),
]

grammar = Grammar(vn, vt, p, 'S')
grammar1 = Grammar(vn1, vt1, p1, 'S')

grammar1.printGrammar()
cnf = grammar1.ChomskyNormalForm(show_proccess=False)
print('After transformation')
cnf.printGrammar()
