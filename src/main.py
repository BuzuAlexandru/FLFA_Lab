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

vn1 = ['S', 'X' 'A', 'B', 'C', 'D']
vt1 = ['a', 'b']
p1 = [
    Production('S', 'B'),
    Production('A', 'aX'),
    Production('A', 'bX'),
    Production('X', 'ε'),
    Production('X', 'BX'),
    Production('X', 'b'),
    Production('B', 'AXaD'),
    Production('C', 'Ca'),
    Production('D', 'aD'),
    Production('D', 'a'),
]

grammar = Grammar(vn, vt, p, 'S')
grammar1 = Grammar(vn1, vt1, p1, 'S')

cnf = grammar1.ChomskyNormalForm(show_proccess=True)
cnf.printGrammar()
