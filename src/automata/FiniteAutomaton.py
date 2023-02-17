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
