class Transition:
    def __init__(self, current, label, nxt):
        self.currentState = current
        self.transitionLabel = label
        self.nextState = nxt
