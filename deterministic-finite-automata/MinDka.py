"""Create DFA from standard input and print minimized DFA."""
class DFA(object):
    """Deterministic final automata."""

    def __init__(self, all_states, symbols, acceptable_states, starting_state, transitions):
        """
        Automata definition.

        :param all_states: set of states (Q)
        :param symbols: set of alphabet symbols (SIGMA)
        :param accaptable_states: set of acceptable states (F)
        :param starting_state: starting state (Q0)
        :param transitions: transitions table dictionary (DELTA)
        """
        self.ALL_STATES = all_states
        self.SYMBOLS = symbols
        self.ACCEPTABLE_STATES = acceptable_states
        self.STARTING_STATE = starting_state
        self.TRANSITIONS = transitions


    def getTransition(self, state, symbol):
        """
        Get next state from transitions table. If state does not exist in transitions table, None is returned.

        :param state: automata state
        :param symbol: alphabet symbol
        :return: state or None
        """
        return self.TRANSITIONS.get((state, symbol))


    def getReachableStates(self):
        """
        Extract only reachable states from set of states.

        :return: set of reachable states
        """
        reachable_states = set([self.STARTING_STATE])

        for symbol in self.SYMBOLS:
            possible_state = self.getTransition(self.STARTING_STATE, symbol)
            if possible_state != None:
                reachable_states.add(possible_state)

        size = 0
        while len(reachable_states) > size:
            size = len(reachable_states)
            new_states = set()
            for state in reachable_states:
                for symbol in self.SYMBOLS:
                    possible_state = self.getTransition(state, symbol)
                    if possible_state != None:
                        new_states.add(possible_state)
            reachable_states.update(new_states)

        return reachable_states


    def removeUnreachableStates(self):
        """Remove unreachable states and all links to them in transitions table."""
        reachable_states = self.getReachableStates()

        self.ALL_STATES = set(state for state in self.ALL_STATES if state in reachable_states)
        self.ACCEPTABLE_STATES = set(state for state in self.ACCEPTABLE_STATES if state in reachable_states)
        self.TRANSITIONS = {k:v for k, v in self.TRANSITIONS.items() if k[0] in reachable_states}


    def sortTuple(self, a, b):
        """
        Get sorted tuple from two items.

        :param a: first item
        :param b: second item
        :return: sorted tuple
        """
        return (a, b) if a < b else (b, a)


    def createMatrix(self):
        """
        Create matrix.

        :return: matrix
        """
        matrix = dict()
        all_states = sorted(self.ALL_STATES)

        for i in range(len(all_states) - 1):
            for j in range(i + 1, len(all_states)):
                # This is already cleaned transitions table
                matrix[self.sortTuple(all_states[i], all_states[j])] = ((all_states[i] in self.ACCEPTABLE_STATES) ^ (all_states[j] in self.ACCEPTABLE_STATES))

        for i in range(len(all_states) - 1):
            for j in range(i + 1, len(all_states)):

                for symbol in self.SYMBOLS:
                    transition1 = self.getTransition(all_states[i], symbol)
                    transition2 = self.getTransition(all_states[j], symbol)

                    if (transition1 != None) and (transition2 != None):
                        if matrix.get(self.sortTuple(transition1, transition2)):
                            matrix[self.sortTuple(all_states[i], all_states[j])] = True

        return matrix


    def findSameStates(self, matrix):
        """
        Calculate same states from given matrix.

        :param matrix: matrix dictionary
        :return: list of tuples representing same states
        """
        same_states = list()
        all_states = sorted(self.ALL_STATES)

        for i in range(len(all_states) - 1):
            for j in range(i + 1, len(all_states)):
                if not matrix.get(self.sortTuple(all_states[i], all_states[j])):
                    same_states.append(self.sortTuple(all_states[i], all_states[j]))

        return same_states


    def minimize(self):
        """
        Minimize DFA.

        :return: new minimized DFA object
        """
        minimizedDFA = DFA(self.ALL_STATES, self.SYMBOLS, self.ACCEPTABLE_STATES, self.STARTING_STATE, self.TRANSITIONS)

        minimizedDFA.removeUnreachableStates()
        matrix = minimizedDFA.createMatrix()
        same_states = minimizedDFA.findSameStates(matrix)

        for state in same_states:
            for symbol in minimizedDFA.SYMBOLS:

                try:
                    del minimizedDFA.TRANSITIONS[(state[1], symbol)]
                except:
                    pass

                try:
                    minimizedDFA.ALL_STATES.remove(state[1])
                except:
                    pass

                try:
                    minimizedDFA.ACCEPTABLE_STATES.remove(state[1])
                except:
                    pass

                if state[1] == minimizedDFA.STARTING_STATE:
                    minimizedDFA.STARTING_STATE = state[0]

        for key in minimizedDFA.TRANSITIONS.keys():
            for state in same_states:
                if minimizedDFA.TRANSITIONS.get(key) == state[1]:
                    minimizedDFA.TRANSITIONS[key] = state[0]

        return minimizedDFA


    def printDFA(self):
        """Print DFA definition."""
        print(",".join(sorted(self.ALL_STATES)))
        print(",".join(sorted(self.SYMBOLS)))
        print(",".join(sorted(self.ACCEPTABLE_STATES)))
        print(self.STARTING_STATE)
        for item in sorted(self.TRANSITIONS.items()):
            print("{},{}->{}".format(item[0][0], item[0][1], item[1]))



def getInputTransitions():
    """
    Get all transitions functions from input.

    :return: Dictionary of transitions functions
    """
    transitions = dict()
    while True:
        try:
            function = input()
            if function == "\n" or function == "": break
            function = function.split("->")
            transitions[tuple(function[0].split(","))] = function[1]
        except:
            break
    return transitions


def main():
    """Automata input and definition."""
    ALL_STATES = set(input().split(","))            # Q
    SYMBOLS = set(input().split(","))               # Alphabet symbols (sigma)
    ACCEPTABLE_STATES = set(input().split(","))     # F is a subset of Q
    STARTING_STATE = input()                        # Q0
    TRANSITIONS = getInputTransitions()             # Transition functions (delta)

    originalDFA = DFA(ALL_STATES, SYMBOLS, ACCEPTABLE_STATES, STARTING_STATE, TRANSITIONS)

    minimizedDFA = originalDFA.minimize()
    minimizedDFA.printDFA()


if __name__ == "__main__":
    main()
