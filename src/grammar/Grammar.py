from random import choice
from grammar.Production import Production
from automata.Transition import Transition
from automata.FiniteAutomaton import FiniteAutomaton
from itertools import combinations
from collections import Counter

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

    def productionToDict(self):
        productionDict = {}
        for i in self.productions:
            if i.leftSide not in productionDict.keys():
                productionDict[i.leftSide] = set()
                productionDict[i.leftSide].add(i.rightSide)
            else:
                productionDict[i.leftSide].add(i.rightSide)

        return productionDict

    def generateWord(self):
        productionDict = self.productionToDict()

        word = self.start
        while not word.islower():
            for i in productionDict.keys():
                if word.find(i) > -1:
                    word = word.replace(i, choice(list(productionDict[i])), 1)

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

    def printGrammar(self):
        print('VN =', str(self.nonTerminalVar).replace("'", ''))
        print('VT =', str(self.terminalVar).replace("'", ''))
        print('P = [')
        prod = self.productionToDict()
        for leftSide in prod.keys():
            print('\t', leftSide,'→', end=' ')
            rules = list(prod[leftSide])
            for rule in rules:
                if rule != rules[-1]:
                    print(rule, end=' | ')
                else:
                    print(rule)
        print(']')

    def isInCNF(self):
        prod = self.productionToDict()

        for leftSide in prod.keys():
            inaccessible = True
            for rule in prod[leftSide]:
                if not ((len(rule) == 1 and rule.islower()) or (len(rule) == 2 and rule.isupper())):

                    return False
                if rule == 'ε':

                    return False
                if rule in self.nonTerminalVar:

                    return False

            if leftSide != self.start:
                for rules in prod.values():
                    for rule1 in rules:
                        if rule1.find(leftSide) != -1:
                            inaccessible = False
                            break
            else: continue

            if inaccessible:
                return False

        return True


    def ChomskyNormalForm(self, show_proccess = False):
        prod = self.productionToDict()
        vn = self.nonTerminalVar.copy()

        if show_proccess:
            print('Intitial production rules')
            for k, v in prod.items():
                print(k, '->', v)

        # auxiliary dict to add changes made to the grammar, for the first 2 steps
        aux = {}

        # 1. remove empty productions
        def createCombinations(prod_rule, leftSide, empty):
            new_rules = set()
            non_empty_symbols = prod_rule.replace(empty, '')
            for i in range(len(non_empty_symbols), len(prod_rule)):
                all_combinations = set(combinations(prod_rule, i))
                for combination in all_combinations:
                    a = list(non_empty_symbols)
                    b = list(combination)
                    test = list((Counter(list(non_empty_symbols)) & Counter(list(combination))).elements())
                    if test == list(non_empty_symbols):
                        new_rules.add(''.join(combination))

            if leftSide in aux.keys():
                aux[leftSide].update(new_rules)
            else:
                aux[leftSide] = new_rules


        def updateProductions():
            for leftSide in prod.keys():
                for key in aux.keys():
                    if leftSide == key:
                        prod[leftSide].update(aux[key])


        for leftSide in prod.keys():
            for rule in prod[leftSide]:
                if rule == 'ε':
                    for leftSide1 in prod.keys():
                        for rule1 in prod[leftSide1]:
                            if len(rule1) > 1 and rule1.find(leftSide) != -1:
                                createCombinations(rule1, leftSide1, leftSide)
                    updateProductions()
                    prod[leftSide].discard('ε')
                    break


        if show_proccess:
            print('\nAfter removing empty productions')
            for k, v in prod.items():
                print(k, '->', v)


        # 2. removing unit productions
        aux = {}

        # while renaming exists eg. A -> B:
        # remove B from A, then get all production rules from B and shove them into A

        def hasUnitProductions(prod_dict):
            for leftSide in prod.keys():
                for rule in prod[leftSide]:
                    if rule in self.nonTerminalVar:
                        return True
            return False

        while hasUnitProductions(prod):
            for leftSide in prod.keys():
                done = False
                for rule in prod[leftSide]:
                    if rule in self.nonTerminalVar:
                        aux[leftSide] = prod[rule]
                        remove_from = leftSide
                        to_remove = rule
                        done = True
                        break
                if done:
                    break

            prod[remove_from].discard(to_remove)
            updateProductions()
            aux = {}



        if show_proccess:
            print('\nAfter removing unit productions')
            for k, v in prod.items():
                print(k, '->', v)

        # 3. remove unproductive symbols. eg. of productive A -> a | aa | abb
        # find all unproductive symbols, remove them, then remove all production rules that contain the unproductive symbols

        unproductive_symbols = set([])

        copy = prod.copy()
        for leftSide in copy.keys():
            unproductive = True
            for rule in prod[leftSide]:
                if rule.islower():
                    unproductive = False
                    break

            if unproductive:
                unproductive_symbols.add(leftSide)
                prod.pop(leftSide)
                vn.remove(leftSide)


        for leftSide in prod.keys():
            rules = prod[leftSide].copy()
            for rule in rules:
                for unproductive_symbol in unproductive_symbols:
                    if rule.find(unproductive_symbol) != -1:
                        prod[leftSide].discard(rule)


        if show_proccess:
            print('\nAfter removing unproductive symbols')
            for k, v in prod.items():
                print(k, '->', v)


        # 4. remove inaccessible symbols
        # check every key of the prod dict if it is present in other production rules

        def rmInaccessibleSymbols():
            aux = prod.copy()
            for leftSide in aux.keys():
                if leftSide == list(prod.keys())[0]:
                    continue

                copy = aux.copy()
                copy.pop(leftSide)
                inaccessible = True
                for rules in copy.values():
                    for rule in rules:
                        if rule.find(leftSide) != -1:
                            inaccessible = False
                            break
                    if not inaccessible:
                        break

                if inaccessible:
                    prod.pop(leftSide)
                    vn.remove(leftSide)


        rmInaccessibleSymbols()

        if show_proccess:
            print('\nAfter removing inaccessible symbols')
            for k, v in prod.items():
                print(k, '->', v)


        '''
        5. convert to CNF
        iterate through all production rules
        a) if a rule is a single terminal or two non-terminals, keep it as is
        b) create rules for all terminal symbols which will then replace the terminals in the existing rules
        c) if a rule has len >= 3, eg. S -> GBAB, separate it into multiple rules, eg. S -> GH, H -> BI, I -> AB
        '''

        inverse_prod = {}

        for terminal in self.terminalVar:
            newNT = 'A'
            while newNT in vn or not newNT.isalpha() or not newNT.isupper():
                newNT = chr(ord(newNT) + 1)

            prod[newNT] = set([terminal])
            inverse_prod[terminal] = newNT
            vn.append(newNT)

        for leftSide in prod.keys():
            rules = prod[leftSide]
            rules_copy = prod[leftSide].copy()
            for rule in rules_copy:
                if len(rule) > 1:
                    rules.discard(rule)
                    new_rule = rule
                    for terminal in self.terminalVar:
                        if rule.find(terminal) != -1:
                            new_rule = new_rule.replace(terminal, inverse_prod[terminal])
                    rules.add(new_rule)

        rmInaccessibleSymbols()

        def hasLongSequence(prod_dict):
            for leftSide in prod.keys():
                for rule in prod[leftSide]:
                    if len(rule) > 2:
                        return True
            return False


        while hasLongSequence(prod):
            prod_copy = prod.copy()
            for leftSide in prod_copy.keys():
                rules = prod[leftSide]
                rules_copy = prod[leftSide].copy()
                for rule in rules_copy:
                    if (len(rule) == 1 and rule.islower()) or (len(rule) == 2 and rule.isupper()):
                        continue
                    elif len(rule) >= 3:
                        str_partition = rule.partition(rule[0])
                        to_replace = str_partition[2]

                        if to_replace in inverse_prod.keys():
                            rules.discard(rule)
                            rules.add(rule.replace(to_replace, inverse_prod[to_replace]))

                        else:
                            newNT = chr(ord(vn[-1]) + 1)
                            while newNT in vn or not newNT.isalpha() or not newNT.isupper():
                                newNT = chr(ord(newNT) + 1)

                            vn.append(newNT)
                            prod[newNT] = set([to_replace])
                            inverse_prod[to_replace] = newNT

                            rules.discard(rule)
                            rules.add(rule.replace(to_replace, newNT))


        if show_proccess:
            print('\nAfter final transformation')
            for k, v in prod.items():
                print(k, '->', v)

        p = []
        for leftSide in prod.keys():
            for rule in prod[leftSide]:
                p.append(Production(leftSide, rule))

        return Grammar(vn, self.terminalVar, p, list(prod.keys())[0])
