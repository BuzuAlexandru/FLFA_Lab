import unittest
from grammar.Grammar import Grammar
from grammar.Production import Production


class TestCNF(unittest.TestCase):
    def test1(self):
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

        grammar = Grammar(vn, vt, p, 'S')
        cnf = grammar.ChomskyNormalForm()
        self.assertFalse(grammar.isInCNF())
        self.assertTrue(cnf.isInCNF())

    def test2(self):
        vn = ['S', 'X', 'A', 'B', 'C', 'D']
        vt = ['a', 'b']
        p = [
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
        cnf = grammar.ChomskyNormalForm()
        self.assertFalse(grammar.isInCNF())
        self.assertTrue(cnf.isInCNF())

    def test3(self):
        vn = ['S', 'A', 'B', 'D']
        vt = ['a', 'b', 'd']
        p = [
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
        cnf = grammar.ChomskyNormalForm()
        self.assertFalse(grammar.isInCNF())
        self.assertTrue(cnf.isInCNF())


if __name__ == '__main__':
    unittest.main()
