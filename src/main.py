from grammar.Grammar import Grammar
from grammar.Production import Production
from automata.FiniteAutomaton import FiniteAutomaton
from automata.Transition import Transition

vn = ['S', 'L', 'D']
vt = ['a', 'b', 'c', 'd', 'e', 'f', 'j']
p = [
    Production('S', 'aS'),
    Production('S', 'bS'),
    Production('S', 'cD'),
    Production('S', 'dL'),
    Production('S', 'e'),
    Production('L', 'eL'),
    Production('L', 'fL'),
    Production('L', 'jD'),
    Production('L', 'e'),
    Production('D', 'eD'),
    Production('D', 'd'),
]

grammar = Grammar(vn, vt, p, 'S')
print(grammar.classify())

vn = ['S', 'L', 'D']
vt = ['a', 'b', 'c', 'd', 'e', 'f', 'j']
p = [
    Production('S', 'aa'),
    Production('S', 'Dc'),
    Production('S', 'c'),
    Production('S', 'L'),
    Production('S', 'e'),
    Production('L', 'eL'),
    Production('D', 'De'),
    Production('D', 'd'),
]

grammar2 = Grammar(vn, vt, p, 'S')
print(grammar2.classify())

q = ['q0', 'q1', 'q2', 'q3']
a = ['a', 'b']
t = [
    Transition('q0', 'a', 'q1'),
    Transition('q0', 'a', 'q2'),
    Transition('q1', 'b', 'q1'),
    Transition('q1', 'a', 'q2'),
    Transition('q2', 'a', 'q1'),
    Transition('q2', 'b', 'q3'),
]
s = 'q0'
f = ['q3']

automata = FiniteAutomaton(q, a, t, s, f)
print('The given automata is a ' + automata.classify())
automata.toGrammar().toFiniteAutomaton().display()
# automata.display()
# automata.toDFA().display()
