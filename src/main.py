from grammar.Grammar import Grammar
from grammar.Production import Production

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

automata = grammar.toFiniteAutomaton()

for i in range(5):
    word = grammar.generateWord()
    if automata.wordIsValid(word):
        print(word, ' valid')
    else:
        print(word, ' invalid')

word = 'bcdef'
if automata.wordIsValid(word):
    print(word, ' valid')
else:
    print(word, ' invalid')
