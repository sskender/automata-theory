global ALL_STATES, SYMBOLS, ACCEPTABLE_STATES, NOT_ACCEPTABLE_STATES, STARTING_STATE, TRANSITIONS


def getInputTransitions():
    """
    Get all transitions functions from input
    :return: Dictionary of transitions functions
    """
    transitions = dict()
    while True:
        try:
            function = input()
            if function == "\n" or function == "": break
            function = function.split("->")
            transitions[tuple(function[0].split(","))] = set(function[1].split(","))
        except:
            break
    return transitions


def getNotAcceptableStates():
    """
    Get all not acceptable states
    :return: set of not acceptable states
    """
    return set(ALL_STATES.difference(ACCEPTABLE_STATES))


def getTransitions(state, symbol):
    """
    Get set of next states from transitions table
    If state does not exist in transitions table, empty set is returned
    :param state: automata state
    :param symbol: alphabet symbol
    :return: set of states
    """
    if TRANSITIONS.get((state, symbol)) != None:
        return set(TRANSITIONS.get((state, symbol)))


def getReachableStates():
    """
    Extract only reachable states from set of states
    :return: set of states
    """
    reachable_states = set([STARTING_STATE])

    for symbol in SYMBOLS:
        reachable_states.update(getTransitions(STARTING_STATE, symbol))

    size = 0
    while len(reachable_states) > size:
        size = len(reachable_states)
        new_states = set()
        for state in reachable_states:
            for symbol in SYMBOLS:
                new_states.update(getTransitions(state, symbol))
        reachable_states.update(new_states)

    return reachable_states


def printDFA():
    """
    Print minimized DFA
    """
    print(",".join(sorted(ALL_STATES)))
    print(",".join(sorted(SYMBOLS)))
    print(",".join(sorted(ACCEPTABLE_STATES)))
    print(STARTING_STATE)
    for state in sorted(ALL_STATES):
        for symbol in sorted(SYMBOLS):
            print("{},{}->{}".format(state, symbol, list(getTransitions(state, symbol))[0]))


# Definition
# Input format
ALL_STATES = set(input().split(","))                        # Q
SYMBOLS = set(input().split(","))                           # Alphabet symbols (sigma)
ACCEPTABLE_STATES = set(input().split(","))                 # F is a subset of Q
STARTING_STATE = input()                                    # Q0
TRANSITIONS = getInputTransitions()                         # Transition functions (delta)
NOT_ACCEPTABLE_STATES = getNotAcceptableStates()
REACHABLE_STATES = getReachableStates()


def main():
    printDFA()


if __name__ == "__main__":
    main()

