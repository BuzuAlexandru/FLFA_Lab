# Laboratory work nr.2
# Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.
### University: Technical University of Moldova
### Course: Formal Languages & Finite Automata
### Author: Alexandru Buzu, FAF 212 (variant 4)

---

## Objectives:

1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:
    a. Provide a function in the grammar type/class that could classify the grammar based on Chomsky hierarchy.

3. According to the variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

    a. Implement conversion of a finite automaton to a regular grammar.

    b. Determine whether the FA is deterministic or non-deterministic.

    c. Implement some functionality that would convert an NDFA to a DFA.
    
    d. Represent the finite automaton graphically (Optional, and can be considered as a __*bonus point*__):
     

## Implementation description
* For the function that classifies the grammar based on Chomsky's 
hierarchy, I basically split it in two halves, one to differentiate between
type 0 and 1, and the second one between type 2 and 3.
  - If at least one production has two or more terminals and/or 
  non-terminals on the left side and no empty string on the right side,
  then it's Type 1.
  - If at least one production has two or more terminals and/or 
  non-terminals on the left side and empty string is on the right side,
  then it's Type 0.

```python
for i in self.productions:
    if len(i.leftSide) > 1:
        aux1 = True
    if i.rightSide.find('ε') > -1 :
        aux2 = True

if aux1 and aux2:
    return 'Type 0'
elif aux1 and not aux2:
    return 'Type 1'
```
* type 2, 1
```python
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
```
* FA to grammar
```python
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
```
* determinism
```python
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
```
* nfa to dfa
```python
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
```
* represent graphically
```python
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
```

![]()
## Screenshots

![]()
## Conclusions

## References
* Course lecture "Regular language. Finite automata"
* https://en.wikipedia.org/wiki/Chomsky_hierarchy
* https://graphviz.readthedocs.io/en/stable/manual.html
