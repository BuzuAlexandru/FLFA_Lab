from random import choice
from automata.Transition import Transition
from automata.FiniteAutomaton import FiniteAutomaton
class Grammar:
    def __init__(self, nterm, term, prod, strt):
        self.nonTerminalVar = nterm
        self.terminalVar = term
        self.productions = prod
        self.start = strt

    def classify(self):
        aux1 = False
        aux2 = False
        for i in self.productions:
            if len(i.leftSide) > 1:
                aux1 = True
            if i.rightSide.find('ε') > -1 :
                aux2 = True

        if aux1 and aux2:
            return 'Type 0'
        elif aux1 and not aux2:
            return 'Type 1'

        c = 0
        for i in self.productions:
            c += 1
            if i.rightSide[0].isupper() and len(i.rightSide) > 1:
                linearity1 = 'L'
                break
            elif i.rightSide[-1].isupper() and len(i.rightSide) > 1:
                linearity1 = 'R'
                break
            elif c == len(self.productions):
                linearity1 = ''

        for i in self.productions:
            temp = sum(1 for c in i.rightSide if c.isupper())
            if temp > 1:
                return 'Type 2'
            elif temp == 1 and i.rightSide[0].islower() and i.rightSide[-1].islower():
                return 'Type 2'

            if i.rightSide[0].isupper() and len(i.rightSide) > 1:
                linearity2 = 'L'
            elif i.rightSide[-1].isupper() and len(i.rightSide) > 1:
                linearity2 = 'R'
            else:
                linearity2 = linearity1

            if linearity1 != linearity2:
                return 'Type 2'

        return 'Type 3'



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
        finalStates = ['Qf']
        transitions = []
        for i in self.productions:
            if len(i.rightSide) == 2:
                transitions.append(Transition(i.leftSide, i.rightSide[0], i.rightSide[1]))
            else:
                transitions.append(Transition(i.leftSide, i.rightSide, 'Qf'))

        return FiniteAutomaton(self.nonTerminalVar + finalStates, self.terminalVar, transitions, self.start, finalStates)
