from random import choice
from automata.Transition import Transition
from automata.FiniteAutomaton import FiniteAutomaton
class Grammar:
    def __init__(self, nterm, term, prod, strt):
        self.nonTerminalVar = nterm
        self.terminalVar = term
        self.productions = prod
        self.start = strt

    def generateWord(self):
        productionDict = {}
        for i in self.productions:
            if i.leftSide not in productionDict.keys():
                productionDict[i.leftSide] = []
                productionDict[i.leftSide].append(i.rightSide)
            else:
                productionDict[i.leftSide].append(i.rightSide)

        word = self.start
        while not word.islower():
            for i in productionDict.keys():
                if word.find(i) > -1:
                    word = word.replace(i, choice(productionDict[i]), 1)

        return word
    def toFiniteAutomaton(self):
        finalStates = []
        transitions = []
        c = 0
        for i in self.productions:
            if len(i.rightSide) == 2:
                transitions.append(Transition(i.leftSide, i.rightSide[1], i.rightSide[0]))
            else:
                c += 1
                transitions.append(Transition(i.leftSide, 'q' + str(c), i.rightSide))
                finalStates.append('q' + str(c))

        return FiniteAutomaton(self.nonTerminalVar, self.terminalVar, transitions, self.start, finalStates)
