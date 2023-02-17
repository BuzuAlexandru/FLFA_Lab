class Transition:
    def __init__(self, current, nxt, label):
        self.currentState = current
        self.nextState = nxt
        self.transitionLabel = label
