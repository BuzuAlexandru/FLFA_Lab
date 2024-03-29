from graphviz import Digraph
import tempfile


class FiniteAutomaton:
    def __init__(self, possible, alphabet, transitions, strt, fin):
        self.possibleStates = possible
        self.alphabet = alphabet
        self.transitions = transitions
        self.initialState = strt
        self.finalStates = fin

    def wordIsValid(self, word):
        state = self.initialState

        for i in range(len(word)):
            if word[i] not in self.alphabet:
                return False

            for j in self.transitions:
                if j.currentState == state and j.transitionLabel == word[i]:
                    if i != len(word) - 1:
                        state = j.nextState
                        break
                    elif i == len(word) - 1 and j.nextState not in self.finalStates:
                        continue
                    elif i == len(word) - 1 and j.nextState in self.finalStates:
                        state = j.nextState
                        break

            if state in self.finalStates and i != len(word) - 1:
                return False

        if state in self.finalStates:
            return True
        else:
            return False

    def toGrammar(self):
        nonTerminal = self.possibleStates
        for i in self.finalStates:
            nonTerminal.remove(i)
        terminal = self.alphabet
        from grammar.Grammar import Grammar
        from grammar.Production import Production
        production = []
        for i in self.transitions:
            if i.nextState in self.finalStates:
                production.append(Production(chr(nonTerminal.index(i.currentState) + 65), i.transitionLabel))
            else:
                production.append(Production(chr(nonTerminal.index(i.currentState) + 65), i.transitionLabel + chr(nonTerminal.index(i.nextState) + 65)))

        start = chr(nonTerminal.index(self.initialState) + 65)

        for i in range(len(nonTerminal)):
            nonTerminal[i] = chr(i + 65)

        return Grammar(nonTerminal, terminal, production, start)

    def classify(self):
        for i in self.transitions:
            if i.transitionLabel == 'ε':
                return 'NFA'
            count = 0
            for j in self.transitions:
                if i.currentState == j.currentState and i.transitionLabel == j.transitionLabel:
                    count += 1
                if count > 1:
                    return 'NFA'
        return 'DFA'

    def display(self):
        f = Digraph()
        f.attr(rankdir="LR")

        f.node("Initial", label="", shape="point")
        f.attr('node', shape='doublecircle')
        for i in self.finalStates:
            f.node(i)

        f.attr('node', shape='circle')
        for i in self.possibleStates:
            if i not in self.finalStates:
                f.node(i)

        f.edge("Initial", self.initialState)
        for i in self.transitions:
            f.edge(i.currentState, i.nextState, label=i.transitionLabel)

        f.view(tempfile.mktemp('.gv'))

    def toDFA(self):
        if self.classify() == 'DFA':
            return self

        nfa_dict = {}
        for i in self.possibleStates:
            nfa_dict.update({(i,): {}})
            for j in self.alphabet:
                nfa_dict[(i,)].update({j: set()})

        for i in self.transitions:
            nfa_dict[(i.currentState,)][i.transitionLabel].add(i.nextState)

        def hasUndefinedStates():
            for x in nfa_dict.values():
                for y in x.keys():
                    z = x[y]
                    if len(z) > 0 and tuple(z) not in nfa_dict.keys():
                        return True
            return False

        test = {('q0',): {'a': {'q1', 'q2'}, 'b': {}}}
        deadState = False
        while hasUndefinedStates():
            temp_dict = {}
            for transition in nfa_dict.values():
                for tLabel in transition.keys():
                    newState = transition[tLabel]
                    if len(newState) == 0:
                        deadState = True

                    if len(newState) > 0 and tuple(newState) not in nfa_dict.keys():
                        temp_dict[tuple(newState)] = {}
                        for j in self.alphabet:
                            temp_dict[tuple(newState)].update({j: set()})

                        for i in newState:
                            for j in self.alphabet:
                                temp_dict[tuple(newState)][j].update(nfa_dict[(i,)][j])

            nfa_dict.update(temp_dict)

        states = []
        fStates = []
        for i in nfa_dict.keys():
            aux = str(set(i)).replace("'", '')
            states.append(aux)
            for j in i:
                if j in self.finalStates:
                    fStates.append(aux)
                    break

        if deadState:
            states.append('ϕ')
            nfa_dict['ϕ'] = {}
            for i in self.alphabet:
                nfa_dict['ϕ'].update({i: 'ϕ'})

        for transition in nfa_dict.values():
            for tLabel in transition.keys():
                newState = transition[tLabel]
                if len(newState) == 0:
                    transition[tLabel] = 'ϕ'

        from automata.Transition import Transition
        from automata.FiniteAutomaton import FiniteAutomaton
        transitions = []
        for transition in nfa_dict.keys():
            for tLabel in nfa_dict[transition].keys():
                if transition == 'ϕ':
                    transitions.append(Transition(transition,
                                                  tLabel,
                                                  str(nfa_dict[transition][tLabel]).replace("'", '')))
                else:
                    transitions.append(Transition(str(set(transition)).replace("'", ''),
                                                  tLabel,
                                                  str(nfa_dict[transition][tLabel]).replace("'", '')))

        return FiniteAutomaton(states, self.alphabet, transitions, str({self.initialState}).replace("'", ''), fStates)
